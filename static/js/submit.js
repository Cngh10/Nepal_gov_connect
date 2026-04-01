/**





submit.js - Nepal Public-Gov Connect







This script handles camera permissions, instant photo capture, 



video recording, and form submission logic for the complaint system.
 */

document.addEventListener('DOMContentLoaded', () => {
    const videoElement = document.getElementById('camera-preview');
    const captureBtn = document.getElementById('capture-photo-btn');
    const recordBtn = document.getElementById('record-video-btn');
    const photoThumbnail = document.getElementById('photo-thumbnail');
    const complaintForm = document.getElementById('complaint-form');
    const locationBtn = document.getElementById('detect-location-btn');
    const locationInput = document.getElementById('location-input');

let stream = null;
let mediaRecorder = null;
let recordedChunks = [];

// --- Camera & Preview Logic ---
async function startCamera() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        if (videoElement) {
            videoElement.srcObject = stream;
            videoElement.classList.remove('hidden');
        }
        console.log("Camera started successfully.");
    } catch (err) {
        console.error("Error accessing camera: ", err);
        alert("Could not access camera. Please ensure you have given permission.");
    }
}

// Initialize camera on page load if the preview element exists
if (videoElement) {
    startCamera();
}

// --- Instant Photo Capture ---
if (captureBtn) {
    captureBtn.addEventListener('click', () => {
        const canvas = document.createElement('canvas');
        canvas.width = videoElement.videoWidth;
        canvas.height = videoElement.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
        
        const imageData = canvas.toDataURL('image/png');
        if (photoThumbnail) {
            photoThumbnail.src = imageData;
            photoThumbnail.classList.remove('hidden');
            console.log("Photo captured.");
        }
    });
}

// --- Video Recording Logic ---
if (recordBtn) {
    recordBtn.addEventListener('click', () => {
        if (!mediaRecorder || mediaRecorder.state === 'inactive') {
            recordedChunks = [];
            mediaRecorder = new MediaRecorder(stream);
            
            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) recordedChunks.push(event.data);
            };

            mediaRecorder.onstop = () => {
                const blob = new Blob(recordedChunks, { type: 'video/webm' });
                const videoURL = URL.createObjectURL(blob);
                console.log("Video recording saved:", videoURL);
                alert("Video recorded successfully!");
            };

            mediaRecorder.start();
            recordBtn.innerHTML = '<span class="material-icons text-red-600 animate-pulse">stop</span> Stop Recording';
            console.log("Recording started...");
        } else {
            mediaRecorder.stop();
            recordBtn.innerHTML = '<span class="material-icons">videocam</span> Record & Post';
            console.log("Recording stopped.");
        }
    });
}

// --- Location Detection Simulation ---
if (locationBtn) {
    locationBtn.addEventListener('click', () => {
        locationBtn.innerHTML = '<span class="material-icons animate-spin">refresh</span> Locating...';
        
        // Simulating a GPS delay
        setTimeout(() => {
            const simulatedLocation = "Kathmandu, Nepal (27.7172° N, 85.3240° E)";
            if (locationInput) {
                locationInput.value = simulatedLocation;
            }
            locationBtn.innerHTML = '<span class="material-icons">my_location</span> Location Detected';
            locationBtn.classList.add('bg-green-100', 'text-green-700');
        }, 1500);
    });
}

// --- Form Submission Flow ---
if (complaintForm) {
    complaintForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Collect form data
        const formData = new FormData(complaintForm);
        const data = {
            content: formData.get('description') || formData.get('subject'),  // Use description or subject as content
            type: 'COMPLAINT',
            location_tag: formData.get('location-tag') || '',
            status: 'PENDING'
        };

        try {
            // Submit to API
            const response = await fetch('/api/feed/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                // Show Success Notification
                const successMsg = document.createElement('div');
                successMsg.className = "fixed bottom-10 left-1/2 transform -translate-x-1/2 bg-green-600 text-white px-6 py-3 rounded-full shadow-2xl z-50 flex items-center gap-2 animate-bounce";
                successMsg.innerHTML = '<span class="material-symbols-outlined">check_circle</span> Complaint Submitted Successfully!';
                document.body.appendChild(successMsg);

                // Redirect to feed after 3 seconds
                setTimeout(() => {
                    window.location.href = "/feed/";
                }, 3000);
            } else {
                alert('Failed to submit complaint. Please try again.');
            }
        } catch (error) {
            console.error('Error submitting complaint:', error);
            alert('Error submitting complaint. Please try again.');
        }
    });
}

});