from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import glob

class Command(BaseCommand):
    help = 'Upload multiple static assets to S3'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='File path or directory with wildcard support (e.g., /path/to/*.png)')
        parser.add_argument('--folder', type=str, default='static/images', help='S3 folder path (default: static/images)')
        parser.add_argument('--overwrite', action='store_true', help='Overwrite existing files')

    def handle(self, *args, **options):
        path = options['path']
        folder = options['folder'].strip('/')
        overwrite = options['overwrite']

        # Get list of files
        if os.path.isdir(path):
            files = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        else:
            files = glob.glob(path)

        if not files:
            self.stdout.write(self.style.ERROR('No files found!'))
            return

        self.stdout.write(self.style.SUCCESS(f'Found {len(files)} file(s) to upload...'))

        uploaded = 0
        skipped = 0
        errors = 0

        for file_path in files:
            filename = os.path.basename(file_path)
            s3_path = f"{folder}/{filename}"

            # Check if file exists
            if not overwrite and default_storage.exists(s3_path):
                self.stdout.write(self.style.WARNING(f'⊘ Skipped (already exists): {filename}'))
                skipped += 1
                continue

            try:
                with open(file_path, 'rb') as f:
                    file_content = f.read()
                    saved_path = default_storage.save(s3_path, ContentFile(file_content))
                    file_url = default_storage.url(saved_path)

                self.stdout.write(self.style.SUCCESS(f'✓ Uploaded: {filename}'))
                self.stdout.write(f'  URL: {file_url}')
                uploaded += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Error uploading {filename}: {str(e)}'))
                errors += 1

        # Summary
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('═' * 50))
        self.stdout.write(self.style.SUCCESS(f'Summary:'))
        self.stdout.write(self.style.SUCCESS(f'  Uploaded: {uploaded}'))
        if skipped > 0:
            self.stdout.write(self.style.WARNING(f'  Skipped: {skipped}'))
        if errors > 0:
            self.stdout.write(self.style.ERROR(f'  Errors: {errors}'))
