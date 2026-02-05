// Starfield Animation
const canvas = document.getElementById('starfield');
const ctx = canvas.getContext('2d');

// Set canvas size
function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
resizeCanvas();
window.addEventListener('resize', resizeCanvas);

// Star properties
const stars = [];
const numStars = 100;
const speed = 0.5;

// Initialize stars
function initStars() {
    for (let i = 0; i < numStars; i++) {
        stars.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            z: Math.random() * 1000,
            size: Math.random() * 2 + 1
        });
    }
}

// Animation loop
function animate() {
    ctx.fillStyle = 'rgba(10, 10, 20, 0.1)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    for (let i = 0; i < stars.length; i++) {
        const star = stars[i];
        
        // Move star
        star.z -= speed;
        
        // Reset if off screen
        if (star.z <= 0) {
            star.z = 1000;
            star.x = Math.random() * canvas.width;
            star.y = Math.random() * canvas.height;
        }
        
        // Calculate position
        const x = star.x / (star.z / 100);
        const y = star.y / (star.z / 100);
        const size = star.size * (1 - star.z / 1000);
        
        // Draw star
        ctx.fillStyle = `rgba(255, 255, 255, ${1 - star.z / 1000})`;
        ctx.beginPath();
        ctx.arc(x, y, size, 0, Math.PI * 2);
        ctx.fill();
    }
    
    requestAnimationFrame(animate);
}

// Start animation
initStars();
animate();
