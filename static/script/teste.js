// scripts.js
document.addEventListener('DOMContentLoaded', function() {
    const editButton = document.getElementById('edit-button');
    const editForm = document.getElementById('edit-form');
    const profileInfo = document.getElementById('profile-info');
    const cancelButton = document.getElementById('cancel-button');

    editButton.addEventListener('click', function() {
        profileInfo.style.display = 'none';
        editForm.style.display = 'block';
    });

    cancelButton.addEventListener('click', function() {
        profileInfo.style.display = 'block';
        editForm.style.display = 'none';
    });
});
