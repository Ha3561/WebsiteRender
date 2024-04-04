// script.js

// Function to update time remaining and today's date every second
function updateTime() {
    const timeRemainingElement = document.getElementById('time-remaining').querySelector('span');
    const todayDateElement = document.getElementById('today-date').querySelector('span');

    // Update time remaining dynamically
    setInterval(() => {
        const currentTime = new Date();
        const endOfDay = new Date();
        endOfDay.setHours(23, 59, 59, 999); // Set end of day time
        const remainingTime = endOfDay - currentTime;

        const hoursRemaining = Math.floor(remainingTime / (1000 * 60 * 60));
        const minutesRemaining = Math.floor((remainingTime % (1000 * 60 * 60)) / (1000 * 60));
        const secondsRemaining = Math.floor((remainingTime % (1000 * 60)) / 1000);

        timeRemainingElement.textContent = `${hoursRemaining}h ${minutesRemaining}m ${secondsRemaining}s`;
    }, 1000); // Update every second

    // Update today's date dynamically
    const currentDate = new Date();
    const formattedDate = currentDate.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
    });
    todayDateElement.textContent = formattedDate;
} 

// Get all elements with the class 'time-left'
// Get all elements with the class 'time-left'
const timeLeftElements = document.querySelectorAll('.time-left');

// Function to update the due in time
function updateDueInTime() {
    timeLeftElements.forEach(element => {
        const dueInSpan = element.querySelector('span');
        if (dueInSpan) {
            let dueIn = parseInt(dueInSpan.textContent);
            if (!isNaN(dueIn) && dueIn > 0) {
                dueInSpan.textContent = dueIn - 1;
            } else if (dueIn <= 0) {
                dueInSpan.textContent = 'Expired';
                // Optionally, you can hide or style the expired deadline differently
                element.closest('li').classList.add('expired');
            }
        }
    });
}

// Update due in time every second
setInterval(updateDueInTime, 1000);
setInterval(updateDueInTime, 1000);

// Call updateTime function when the page is loaded
window.addEventListener('load', updateTime);
