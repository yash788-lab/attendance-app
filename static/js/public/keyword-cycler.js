/* static/js/public/keyword-cycler.js */

document.addEventListener('DOMContentLoaded', () => {
    const cycler = document.querySelector('.pub-hero__keyword-cycler');
    if (!cycler || !cycler.dataset.words) return;

    const words = JSON.parse(cycler.dataset.words);
    let index = 0;

    function cycle() {
        cycler.classList.add('is-exiting');
        
        setTimeout(() => {
            index = (index + 1) % words.length;
            cycler.textContent = words[index];
            cycler.classList.remove('is-exiting');
            cycler.classList.add('is-entering');
            
            setTimeout(() => {
                cycler.classList.remove('is-entering');
            }, 400); // Duration of entering animation
        }, 300); // Duration of exiting animation
    }

    setInterval(cycle, 2500);
});
