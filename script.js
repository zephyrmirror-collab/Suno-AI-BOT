document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const captureArea = document.getElementById('capture-area');
    const styleSelect = document.getElementById('style-select');

    const inputName = document.getElementById('input-name');
    const inputMessage = document.getElementById('input-message');
    const inputTime = document.getElementById('input-time');
    const inputAvatar = document.getElementById('input-avatar');
    const btnDownload = document.getElementById('btn-download');

    const previewName = document.getElementById('preview-name');
    const previewText = document.getElementById('preview-text');
    const previewTime = document.getElementById('preview-time');
    const previewAvatar = document.getElementById('preview-avatar');

    // State
    let currentTheme = 'theme-tg-dark';

    // Helper: Update Theme
    function updateTheme(newTheme) {
        captureArea.classList.remove(currentTheme);
        captureArea.classList.add(newTheme);
        currentTheme = newTheme;

        // Adjust Avatar Border Radius based on theme if needed
        // iOS avatars are usually circular, Telegram also.
        // But message bubbles change heavily.
    }

    // Event Listeners: Style
    styleSelect.addEventListener('change', (e) => {
        updateTheme(e.target.value);
    });

    // Event Listeners: Text Inputs
    inputName.addEventListener('input', (e) => {
        previewName.textContent = e.target.value;
    });

    inputMessage.addEventListener('input', (e) => {
        // preserve newlines
        previewText.innerText = e.target.value;
    });

    inputTime.addEventListener('input', (e) => {
        previewTime.textContent = e.target.value;
    });

    // Event Listener: Avatar Upload
    inputAvatar.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(event) {
                previewAvatar.src = event.target.result;
            }
            reader.readAsDataURL(file);
        }
    });

    // Event Listener: Download
    btnDownload.addEventListener('click', () => {
        // Feedback to user
        const originalText = btnDownload.innerHTML;
        btnDownload.innerHTML = '<i class="fas fa-spinner fa-spin"></i> <span>Generating...</span>';
        btnDownload.disabled = true;

        html2canvas(captureArea, {
            useCORS: true,
            scale: 3, // High resolution
            backgroundColor: null // Use CSS background
        }).then(canvas => {
            const link = document.createElement('a');
            link.download = `fake-post-${Date.now()}.png`;
            link.href = canvas.toDataURL('image/png');
            link.click();

            // Reset button
            btnDownload.innerHTML = originalText;
            btnDownload.disabled = false;
        }).catch(err => {
            console.error('Capture failed:', err);
            alert('Failed to generate image. Check console for details.');
            btnDownload.innerHTML = originalText;
            btnDownload.disabled = false;
        });
    });
});
