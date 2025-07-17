document.addEventListener('DOMContentLoaded', function() {
    const showHideIcon = document.querySelector('.show-hide-icon');
    const passwordField = document.querySelector('#password');
    
    showHideIcon.addEventListener('click', function() {
        if (passwordField.type === 'password') {
            passwordField.type = 'text';
        } else {
            passwordField.type = 'password';
        }
    });
});
