const interval = setInterval(() => {
    const loadMoreButton = document.querySelector('.scaffold-finite-scroll__load-button');

    if (loadMoreButton && !loadMoreButton.disabled) {
        loadMoreButton.click();
        console.log("▶ Chargement d'un lot de profils...");
    } else if (!loadMoreButton) {
        console.log("✅ Tous les profils ont été chargés ou le bouton n'est plus visible.");
        clearInterval(interval);
    }
}, 3000); // Essaye toutes les 3 secondes
