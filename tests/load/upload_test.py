"""
Locust performance test for file upload functionality
"""
import random
import string
from io import BytesIO
from locust import HttpUser, task, between


class FileUploadUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Called when a simulated user starts running"""
        # Check if the API is healthy
        response = self.client.get("/health")
        if response.status_code != 200:
            print(f"Health check failed: {response.status_code}")
    
    @task(3)
    def upload_small_file(self):
        """Upload a small test file (1KB)"""
        content = self._generate_random_content(1024)
        filename = f"test_small_{random.randint(1000, 9999)}.txt"
        
        with self.client.post(
            "/upload",
            files={"file": (filename, BytesIO(content.encode()), "text/plain")},
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
                # Store filename for potential download test
                self.uploaded_files = getattr(self, 'uploaded_files', [])
                self.uploaded_files.append(filename)
            else:
                response.failure(f"Upload failed: {response.status_code}")
    
    @task(2)
    def upload_medium_file(self):
        """Upload a medium test file (100KB)"""
        content = self._generate_random_content(102400)
        filename = f"test_medium_{random.randint(1000, 9999)}.txt"
        
        with self.client.post(
            "/upload",
            files={"file": (filename, BytesIO(content.encode()), "text/plain")},
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
                self.uploaded_files = getattr(self, 'uploaded_files', [])
                self.uploaded_files.append(filename)
            else:
                response.failure(f"Upload failed: {response.status_code}")
    
    @task(1)
    def upload_large_file(self):
        """Upload a large test file (1MB)"""
        content = self._generate_random_content(1048576)
        filename = f"test_large_{random.randint(1000, 9999)}.txt"
        
        with self.client.post(
            "/upload",
            files={"file": (filename, BytesIO(content.encode()), "text/plain")},
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
                self.uploaded_files = getattr(self, 'uploaded_files', [])
                self.uploaded_files.append(filename)
            else:
                response.failure(f"Upload failed: {response.status_code}")
    
    @task(2)
    def list_files(self):
        """List all uploaded files"""
        with self.client.get("/files", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"List files failed: {response.status_code}")
    
    @task(1)
    def download_file(self):
        """Download a previously uploaded file"""
        uploaded_files = getattr(self, 'uploaded_files', [])
        if not uploaded_files:
            return
        
        filename = random.choice(uploaded_files)
        with self.client.get(f"/download/{filename}", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 404:
                # File might have been deleted or doesn't exist
                response.success()
            else:
                response.failure(f"Download failed: {response.status_code}")
    
    @task(1)
    def get_health(self):
        """Check system health"""
        with self.client.get("/health", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Health check failed: {response.status_code}")
    
    def _generate_random_content(self, size: int) -> str:
        """Generate random content of specified size"""
        return ''.join(random.choices(string.ascii_letters + string.digits + '\n', k=size))