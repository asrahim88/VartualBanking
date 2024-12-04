// Toggle password visibility for Old Password field
document.getElementById('togglePasswordOld').addEventListener('click', function () {
    var passwordField = document.getElementById('old_password');
    var icon = document.querySelector('#togglePasswordOld i');
    
    if (passwordField.type === 'password') {
        passwordField.type = 'text';  // Change to text to show password
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        passwordField.type = 'password';  // Change to password to hide it
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
});

// Toggle password visibility for New Password field
document.getElementById('togglePasswordNew').addEventListener('click', function () {
    var passwordField = document.getElementById('new_password1');
    var icon = document.querySelector('#togglePasswordNew i');
    
    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        passwordField.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
});

// Toggle password visibility for Confirm New Password field
document.getElementById('togglePasswordConfirm').addEventListener('click', function () {
    var passwordField = document.getElementById('new_password2');
    var icon = document.querySelector('#togglePasswordConfirm i');
    
    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        passwordField.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
});