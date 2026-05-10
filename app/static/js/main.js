document.querySelectorAll('.delete-form').forEach((form) => {
    form.addEventListener('submit', (event) => {
        const confirmar = confirm('¿Seguro que deseas eliminar esta tarea? Esta acción no se puede deshacer.');
        if (!confirmar) {
            event.preventDefault();
        }
    });
});

const searchInput = document.querySelector('#q');
const taskCards = document.querySelectorAll('.task-card');

if (searchInput && taskCards.length > 0) {
    searchInput.addEventListener('input', () => {
        const term = searchInput.value.toLowerCase().trim();
        taskCards.forEach((card) => {
            const text = card.dataset.title || card.textContent.toLowerCase();
            card.classList.toggle('hidden-by-search', term && !text.includes(term));
        });
    });
}

document.querySelectorAll('.category-card').forEach((card) => {
    card.addEventListener('mouseenter', () => {
        card.style.transform = 'translateY(-4px) scale(1.01)';
    });
    card.addEventListener('mouseleave', () => {
        card.style.transform = '';
    });
});
