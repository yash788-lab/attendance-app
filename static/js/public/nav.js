document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.querySelector('.pub-nav-toggle--menu');
    const overlay = document.querySelector('.pub-nav-overlay');
    const links = document.querySelectorAll('.pub-nav-overlay__link');

    function openNav() {
        if (!toggle || !overlay) return;
        toggle.classList.add('is-active');
        overlay.classList.add('is-open');
        overlay.scrollTop = 0;
        document.body.style.overflow = 'hidden';
        toggle.setAttribute('aria-expanded', 'true');
    }

    function closeNav() {
        if (!toggle || !overlay) return;
        toggle.classList.remove('is-active');
        overlay.classList.remove('is-open');
        document.body.style.overflow = '';
        toggle.setAttribute('aria-expanded', 'false');
    }

    if (toggle) {
        toggle.addEventListener('click', (e) => {
            e.stopPropagation();
            overlay.classList.contains('is-open') ? closeNav() : openNav();
        });
    }

    links.forEach(link => {
        link.addEventListener('click', (e) => {
            if (link.closest('.pub-nav-overlay__dropdown')) {
                if (!link.closest('.pub-nav-overlay__sublist')) return; 
            }
            closeNav();
        });
    });

    const closeBtn = document.querySelector('.pub-nav-overlay__close-btn');
    if (closeBtn) {
        closeBtn.addEventListener('click', closeNav);
    }

    // Scroll Handler Defined Early
    const scrollHandler = () => {
        const header = document.querySelector('.pub-header');
        if (header) {
            header.classList.toggle('is-scrolled', window.scrollY > 50);
        }

        const wavyImage = document.querySelector('.wavy-image');
        if (wavyImage) {
            const rect = wavyImage.getBoundingClientRect();
            if (rect.top < window.innerHeight && rect.bottom > 0) {
                wavyImage.style.transform = `translateY(${window.scrollY * 0.1}px)`;
            }
        }

        const sidebar = document.querySelector('.pub-apply-now');
        if (sidebar) {
            const hero = document.querySelector('.pub-hero');
            if (hero) {
                const heroBottom = hero.offsetTop + hero.offsetHeight;
                if (window.scrollY > heroBottom - 100) {
                    sidebar.style.opacity = '0';
                    sidebar.style.pointerEvents = 'none';
                    sidebar.style.transform = 'translateY(-50%) rotate(-180deg) translateX(-40px)'; // Further push
                    sidebar.style.transition = 'all 0.8s cubic-bezier(0.4, 0, 0.2, 1)'; // Longer/Smoother
                } else {
                    sidebar.style.opacity = '1';
                    sidebar.style.pointerEvents = 'all';
                    sidebar.style.transform = 'translateY(-50%) rotate(-180deg) translateX(0)';
                    sidebar.style.transition = 'all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1)'; // Bouncy in
                }
            }
        }

        // Lottie Scroll Progress
        document.querySelectorAll('.pub-lottie-scroll').forEach(player => {
            // Some players might need a direct access to the Lottie instance
            // We use the seek method if available. 
            const rect = player.getBoundingClientRect();
            const viewHeight = window.innerHeight;
            if (rect.top < viewHeight && rect.bottom > 0) {
                const progress = 1 - (rect.top + rect.height) / (viewHeight + rect.height);
                const boundedProgress = Math.max(0, Math.min(1, progress));
                
                try {
                    // Try different seeking methods depending on player version
                    if (player.getLottie) {
                        const lottie = player.getLottie();
                        if (lottie) lottie.goToAndStop(boundedProgress * lottie.totalFrames, true);
                    } else if (player.seek) {
                        player.seek(boundedProgress * 100 + '%');
                    }
                } catch(e) { }
            }
        });
    };

    window.addEventListener('scroll', scrollHandler, { passive: true });

    // Dark Mode
    const modeToggle = document.getElementById('dark-mode-toggle');
    const modeIcon = document.getElementById('dark-mode-icon');
    
    function applyTheme(theme) {
        if (theme === 'dark') {
            document.documentElement.setAttribute('data-theme', 'dark');
            if (modeIcon) modeIcon.setAttribute('data-lucide', 'sun');
        } else {
            document.documentElement.removeAttribute('data-theme');
            if (modeIcon) modeIcon.setAttribute('data-lucide', 'moon');
        }
        if (window.lucide) lucide.createIcons();
        localStorage.setItem('theme', theme);
    }

    const savedTheme = localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    applyTheme(savedTheme);

    if (modeToggle) {
        modeToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            const currentTheme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
            applyTheme(currentTheme === 'dark' ? 'light' : 'dark');
        });
    }

    // Initial Trigger
    setTimeout(scrollHandler, 200);
});
