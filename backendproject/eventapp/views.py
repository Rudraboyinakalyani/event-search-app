import os
import tarfile
import csv
import time

from django.conf import settings
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from .models import Event
from .serializers import EventSerializer
import os
import tarfile
import csv
import time

from django.conf import settings
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from .models import Event
from .serializers import EventSerializer


class UploadEventsView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        uploaded_file = request.FILES.get('file')
        print(' Uploaded file:', uploaded_file)

        if not uploaded_file:
            return Response({"error": "No file uploaded"}, status=400)

        save_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
        with open(save_path, 'wb+') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

       
        extract_path = os.path.join(settings.MEDIA_ROOT, 'logs_extract')
        os.makedirs(extract_path, exist_ok=True)
        with tarfile.open(save_path, 'r:gz') as tar:
            tar.extractall(path=extract_path)

      
        total_lines = 0
        for file_name in os.listdir(extract_path):
            full_path = os.path.join(extract_path, file_name)
            if os.path.isfile(full_path):
                with open(full_path, 'r') as f:
                    total_lines += sum(1 for _ in f)
        

        events_to_create = []
        skipped = 0

        for file_name in os.listdir(extract_path):
            full_path = os.path.join(extract_path, file_name)

            if os.path.isdir(full_path):
                continue

            with open(full_path, 'r') as file:
                reader = csv.reader(file, delimiter=' ')
                for row in reader:
                    if not row or len(row) < 15:
                        skipped += 1
                        continue

                    try:
                        events_to_create.append(Event(
                            serialno=int(row[0]),
                            version=int(row[1]),
                            account_id=row[2],
                            instance_id=row[3],
                            srcaddr=row[4],
                            dstaddr=row[5],
                            srcport=int(row[6]),
                            dstport=int(row[7]),
                            protocol=row[8],
                            packets=int(row[9]),
                            bytes=int(row[10]),
                            starttime=int(row[11]),
                            endtime=int(row[12]),
                            action=row[13],
                            log_status=row[14],
                            file_name=file_name
                        ))
                    except Exception as e:
                        print(f" Skipping row due to error: {e}")
                        skipped += 1

       
        if events_to_create:
            Event.objects.bulk_create(events_to_create, batch_size=1000)
            print(f" Bulk inserted: {len(events_to_create)} rows")

       

        return Response({
            "message": f"Upload complete.",
           "total_lines": total_lines,
            "imported": len(events_to_create),
            "skipped": skipped
        })





class SearchEventsView(APIView):
    def post(self, request):
        query = request.data.get('query', '')
        start = int(request.data.get('start_time', 0))
        end = int(request.data.get('end_time', 9999999999))
        limit = request.data.get('limit')

        filters = Q(starttime__gte=start) & Q(endtime__lte=end)

        if query:
            filters &= (
                Q(account_id__icontains=query) |
                Q(srcaddr__icontains=query) |
                Q(dstaddr__icontains=query) |
                Q(action__icontains=query)
            )

        queryset = Event.objects.filter(filters)

        if limit is not None:
            try:
                parsed_limit = int(limit)
                if parsed_limit > 0:
                    queryset = queryset[:parsed_limit]
            except ValueError:
                pass

        t1 = time.time()
        serialized = EventSerializer(queryset, many=True)
        t2 = time.time()

        return Response({
            "search_time": round(t2 - t1, 3),
            "results": serialized.data
        })
