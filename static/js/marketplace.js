

document.getElementById('darkModeToggle').addEventListener('click', function() {
    document.body.classList.toggle('dark-mode');
    this.textContent = document.body.classList.contains('dark-mode') ? '☀️ Light Mode' : '🌙 Dark Mode';
});

function filterCreators() {
    const searchInput = document.getElementById('searchInput').value.toLowerCase();
    const categoryFilter = document.getElementById('categoryFilter').value;
    const followerFilter = document.getElementById('followerFilter').value;
    const cards = document.querySelectorAll('.card');

    cards.forEach(card => {
        const name = card.querySelector('h4').textContent.toLowerCase();
        const category = card.querySelector('.tag').textContent;
        const followersText = card.querySelector('p').textContent.split(' ')[0];
        const followers = parseFloat(followersText.replace('K', '')) * 1000;

        let showCard = true;

        if (searchInput && !name.includes(searchInput)) {
            showCard = false;
        }

        if (categoryFilter !== 'All Categories' && category !== categoryFilter) {
            showCard = false;
        }

        if (followerFilter !== 'All Followers') {
            if (followerFilter === 'Under 100K' && followers >= 100000) {
                showCard = false;
            } else if (followerFilter === '100K - 500K' && (followers < 100000 || followers > 500000)) {
                showCard = false;
            } else if (followerFilter === '500K - 1M' && (followers < 500000 || followers > 1000000)) {
                showCard = false;
            } else if (followerFilter === 'Over 1M' && followers <= 1000000) {
                showCard = false;
            }
        }

        card.style.display = showCard ? 'flex' : 'none';
    });
}

// Add real-time search
document.getElementById('searchInput').addEventListener('input', filterCreators);
document.getElementById('categoryFilter').addEventListener('change', filterCreators);
document.getElementById('followerFilter').addEventListener('change', filterCreators);
