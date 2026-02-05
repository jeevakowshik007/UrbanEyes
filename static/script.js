document.addEventListener('DOMContentLoaded', () => {
    const videoFileInput = document.getElementById('videoFile');
    const imageFileInput = document.getElementById('imageFile');
    const videoPreview = document.getElementById('videoPreview');
    const previewVideo = document.getElementById('previewVideo');
    const imagePreview = document.getElementById('imagePreview');
    const previewImage = document.getElementById('previewImage');
    const videoFileName = document.getElementById('videoFileName');
    const imageFileName = document.getElementById('imageFileName');
    const submitBtn = document.getElementById('submitBtn');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const resultsContent = document.getElementById('resultsContent');

    // Handle video file selection
    videoFileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            // Clear image preview
            clearPreview('image');
            
            // Show video preview
            videoFileName.textContent = file.name;
            const videoURL = URL.createObjectURL(file);
            previewVideo.src = videoURL;
            videoPreview.style.display = 'block';
            
            // Highlight container
            document.querySelector('#videoForm .file-label').style.borderColor = '#6366f1';
        }
    });

    // Handle image file selection
    imageFileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            // Clear video preview
            clearPreview('video');
            
            // Show image preview
            imageFileName.textContent = file.name;
            const imageURL = URL.createObjectURL(file);
            previewImage.src = imageURL;
            imagePreview.style.display = 'block';
            
            // Highlight container
            document.querySelector('#imageForm .file-label').style.borderColor = '#6366f1';
        }
    });

    // Handle form submission
    submitBtn.addEventListener('click', async function(e) {
        // Determine which file was selected
        const videoFile = videoFileInput.files[0];
        const imageFile = imageFileInput.files[0];
        
        let file = null;
        let fileName = '';
        
        if (videoFile) {
            file = videoFile;
            fileName = videoFile.name;
        } else if (imageFile) {
            file = imageFile;
            fileName = imageFile.name;
        }
        
        if (!file) {
            alert('Please select a video or image file first.');
            return;
        }

        // Show loading state
        submitBtn.disabled = true;
        submitBtn.querySelector('.btn-content').style.display = 'none';
        submitBtn.querySelector('.btn-loader').style.display = 'inline-block';
        loading.style.display = 'flex'; // Flex for centering
        results.style.display = 'none';

        // Create form data
        const formData = new FormData();
        if (videoFile) {
            formData.append('video', videoFile);
        } else {
            formData.append('image', imageFile);
        }

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            // Hide loading
            loading.style.display = 'none';
            submitBtn.disabled = false;
            submitBtn.querySelector('.btn-content').style.display = 'inline-block';
            submitBtn.querySelector('.btn-loader').style.display = 'none';

            // Check for errors in response
            if (data.error) {
                alert(`Error: ${data.error}`);
                results.style.display = 'none';
                return;
            }

            // Display results
            displayResults(data, fileName);
            
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while analyzing the file. Please try again.');
            loading.style.display = 'none';
            submitBtn.disabled = false;
            submitBtn.querySelector('.btn-content').style.display = 'inline-block';
            submitBtn.querySelector('.btn-loader').style.display = 'none';
            results.style.display = 'none';
        }
    });

    function displayResults(data, fileName) {
        results.style.display = 'block';
        
        const fileExtension = fileName.split('.').pop().toLowerCase();
        const fileType = ['jpg', 'jpeg', 'png', 'gif', 'bmp'].includes(fileExtension) ? 'image' : 'video';
        
        const issues = [
            { name: 'Potholes', key: 'potholes', icon: '<i class="fa-solid fa-road-spikes"></i>' },
            { name: 'Broken Streetlights', key: 'broken_streetlights', icon: '<i class="fa-solid fa-lightbulb"></i>' },
            { name: 'Illegal Garbage Dumping', key: 'garbage_dumping', icon: '<i class="fa-solid fa-trash-can"></i>' },
            { name: 'Drainage Issues', key: 'drainage_issues', icon: '<i class="fa-solid fa-water"></i>' }
        ];
    
        let hasIssues = false;
        let html = '';
    
        issues.forEach(issue => {
            const detected = data[issue.key] || false;
            if (detected) hasIssues = true;
            
            html += `
                <div class="issue-item">
                    <div class="issue-icon" style="color: ${detected ? 'var(--danger)' : 'var(--success)'}">
                        ${issue.icon}
                    </div>
                    <div class="issue-details">
                        <h4>${issue.name}</h4>
                        <span class="status-badge ${detected ? 'status-detected' : 'status-clear'}">
                            ${detected ? '<i class="fa-solid fa-circle-exclamation"></i> Issue Detected' : '<i class="fa-solid fa-check"></i> Clear'}
                        </span>
                    </div>
                </div>
            `;
        });
    
        if (!hasIssues) {
            html += `
                <div class="no-issues-card">
                    <i class="fa-solid fa-shield-heart" style="font-size: 3rem; margin-bottom: 15px;"></i>
                    <p>All systems clear! No issues detected in the ${fileType}.</p>
                </div>
            `;
        }
    
        resultsContent.innerHTML = html;
        
        // Scroll to results
        results.scrollIntoView({ behavior: 'smooth' });
    }
});

// Global function to clear previews (called by onclick in HTML)
window.clearPreview = function(type) {
    if (type === 'video') {
        const input = document.getElementById('videoFile');
        input.value = ''; // Clear input
        document.getElementById('videoPreview').style.display = 'none';
        document.getElementById('previewVideo').src = '';
        document.querySelector('#videoForm .file-label').style.borderColor = 'rgba(255, 255, 255, 0.2)';
    } else if (type === 'image') {
        const input = document.getElementById('imageFile');
        input.value = ''; // Clear input
        document.getElementById('imagePreview').style.display = 'none';
        document.getElementById('previewImage').src = '';
        document.querySelector('#imageForm .file-label').style.borderColor = 'rgba(255, 255, 255, 0.2)';
    }
};
