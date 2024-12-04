// Function to toggle password visibility
function togglePasswordVisibility(passwordFieldId, eyeIconId, eyeSlashIconId) {
    const passwordField = document.getElementById(passwordFieldId);
    const eyeIcon = document.getElementById(eyeIconId);
    const eyeSlashIcon = document.getElementById(eyeSlashIconId);

    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        eyeIcon.classList.add('hidden');
        eyeSlashIcon.classList.remove('hidden');
    } else {
        passwordField.type = 'password';
        eyeIcon.classList.remove('hidden');
        eyeSlashIcon.classList.add('hidden');
    }
}

// Add event listeners for toggle icons
document.getElementById('togglePassword1').addEventListener('click', function() {
    togglePasswordVisibility('id_new_password1', 'togglePassword1', 'togglePassword1Slash');
});
document.getElementById('togglePassword1Slash').addEventListener('click', function() {
    togglePasswordVisibility('id_new_password1', 'togglePassword1', 'togglePassword1Slash');
});

document.getElementById('togglePassword2').addEventListener('click', function() {
    togglePasswordVisibility('id_new_password2', 'togglePassword2', 'togglePassword2Slash');
});
document.getElementById('togglePassword2Slash').addEventListener('click', function() {
    togglePasswordVisibility('id_new_password2', 'togglePassword2', 'togglePassword2Slash');
});