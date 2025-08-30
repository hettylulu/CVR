document.addEventListener('DOMContentLoaded', function() {
    const options = document.querySelectorAll('.option');
    const searchForm = document.getElementById('searchForm');
    options.forEach(option => {
        option.addEventListener('click', function() {
            options.forEach(opt => opt.classList.remove('active'));
            this.classList.add('active');
            document.querySelector('input[name="search_type"]').value = this.value;
        });
    });

    const hiddenInput = document.createElement('input');
    hiddenInput.type = 'hidden';
    hiddenInput.name = 'search_type';
    hiddenInput.value = document.querySelector('.option.active').value;
    searchForm.appendChild(hiddenInput);
});