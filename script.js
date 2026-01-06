document.addEventListener('DOMContentLoaded', () => {
    const nameInput = document.getElementById('name');
    const timeInput = document.getElementById('time');
    const messageInput = document.getElementById('message');
    const avatarInput = document.getElementById('avatar');
    const styleSelect = document.getElementById('style-select');
    const downloadBtn = document.getElementById('download-btn');

    const previewName = document.getElementById('preview-name');
    const previewTime = document.getElementById('preview-time');
    const previewMessage = document.getElementById('preview-message');
    const previewAvatar = document.getElementById('preview-avatar');
    const preview = document.getElementById('preview');

    nameInput.addEventListener('input', () => {
        previewName.textContent = nameInput.value || 'Your Name';
    });

    timeInput.addEventListener('input', () => {
        previewTime.textContent = timeInput.value || '12:00 PM';
    });

    messageInput.addEventListener('input', () => {
        previewMessage.textContent = messageInput.value || 'This is a sample message.';
    });

    avatarInput.addEventListener('change', () => {
        const file = avatarInput.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                previewAvatar.src = e.target.result;
            };
            reader.readAsDataURL(file);
        }
    });

    styleSelect.addEventListener('change', () => {
        preview.className = `p-4 rounded-lg mb-4 ${styleSelect.value}`;
    });

    downloadBtn.addEventListener('click', () => {
        html2canvas(preview, {
            useCORS: true,
            scale: 3
        }).then(canvas => {
            const link = document.createElement('a');
            link.download = 'social-post.png';
            link.href = canvas.toDataURL('image/png');
            link.click();
        });
    });
});
