/* static/js/public/testimonials.js */

document.addEventListener('DOMContentLoaded', () => {
    const track = document.querySelector('[data-carousel]');
    if (!track) return;

    const slides = Array.from(track.querySelectorAll('.pub-testimonials__slide'));
    const dotsContainer = document.querySelector('.pub-testimonials__dots');
    let currentIndex = 0;
    let interval;

    // Create dots
    slides.forEach((_, i) => {
        const dot = document.createElement('button');
        dot.classList.add('pub-testimonials__dot');
        if (i === 0) dot.classList.add('is-active');
        dot.setAttribute('aria-label', `Go to slide ${i + 1}`);
        dot.addEventListener('click', () => goToSlide(i));
        dotsContainer.appendChild(dot);
    });

    const dots = Array.from(dotsContainer.querySelectorAll('.pub-testimonials__dot'));

    function goToSlide(index) {
        slides[currentIndex].classList.remove('is-active');
        dots[currentIndex].classList.remove('is-active');
        
        currentIndex = index;
        
        slides[currentIndex].classList.add('is-active');
        dots[currentIndex].classList.add('is-active');
        
        resetInterval();
    }

    function nextSlide() {
        const next = (currentIndex + 1) % slides.length;
        goToSlide(next);
    }

    function resetInterval() {
        clearInterval(interval);
        interval = setInterval(nextSlide, 5000);
    }

    // Touch support
    let touchStartX = 0;
    let touchEndX = 0;

    track.addEventListener('touchstart', e => {
        touchStartX = e.changedTouches[0].screenX;
    }, {passive: true});

    track.addEventListener('touchend', e => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    }, {passive: true});

    function handleSwipe() {
        if (touchEndX < touchStartX - 50) {
            nextSlide(); // swipe left
        }
        if (touchEndX > touchStartX + 50) {
            const prev = (currentIndex - 1 + slides.length) % slides.length;
            goToSlide(prev); // swipe right
        }
    }

    // Pause on hover
    track.addEventListener('mouseenter', () => clearInterval(interval));
    track.addEventListener('mouseleave', () => resetInterval());

    resetInterval();
});
