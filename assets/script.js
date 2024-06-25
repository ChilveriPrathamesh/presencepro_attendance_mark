document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('uploadButton').addEventListener('click', () => {
        window.location.href = '/upload';
    });
    document.getElementById('checkButton').addEventListener('click', () => {
        window.location.href = '/check';
    });
});
