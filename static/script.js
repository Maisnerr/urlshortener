// Get form and input elements
const form = document.getElementById('urlForm');
const urlInput = document.getElementById('urlInput');
const shortenedUrlDisplay = document.getElementById('shortenedUrl');

form.addEventListener('submit', async (event) => {
    event.preventDefault();  // Prevent form from submitting traditionally
        
    const longUrl = urlInput.value.trim();

    if (!longUrl) {
        alert("Please enter a URL");
        return;
    }

    // Send a POST request to Flask backend
    try {
        const response = await fetch('http://192.168.1.138:5000/shorten', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // Ensure the Content-Type is set to JSON
            },
            body: JSON.stringify({ long_url: longUrl }) // Send the URL as JSON
        });

        // Check if the response is OK (status 200-299)
        if (response.ok) {
            const data = await response.json();
            if (data.short_url) {
                shortenedUrlDisplay.innerHTML = `<a href="${data.short_url}" target="_blank">${data.short_url}</a>`;

                console.log(data.file_url);
                document.getElementById("qrCodeImage").src = data.file_url;
            }
        } else {
            const errorData = await response.json();
            alert(`Error: ${errorData.error || "Something went wrong!"}`);
        }
    } catch (error) {
        console.error('Error during request:', error);
        alert('Something went wrong with the request!');
    }
});
