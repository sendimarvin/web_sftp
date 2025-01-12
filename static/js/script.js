
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('fileSearch');
    const fileList = document.getElementById('fileList');
    const items = fileList.getElementsByTagName('li');

    searchInput.addEventListener('input', function(e) {
        const searchTerm = e.target.value.toLowerCase();

        for (let item of items) {
            const fileName = item.dataset.filename;
            if (fileName.includes(searchTerm)) {
                item.classList.remove('hidden');
            } else {
                item.classList.add('hidden');
            }
        }
    });
});