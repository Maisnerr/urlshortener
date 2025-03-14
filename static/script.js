// Get form and input elements
const form = document.getElementById('urlForm');
const urlInput = document.getElementById('urlInput');
const shortInput = document.getElementById('shortInput');
const shortenedUrlDisplay = document.getElementById('shortenedUrl');

var user = "admin";

form.addEventListener('submit', async (event) => {
    event.preventDefault();  // Prevent form from submitting traditionally
        
    const longUrl = urlInput.value.trim();
    const after = shortInput.value.trim();;

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
            body: JSON.stringify({ long_url: longUrl, after: after }) // Send the URL as JSON
        });

        // Check if the response is OK (status 200-299)
        if (response.ok) {
            const data = await response.json();
            if (data.short_url) {
                shortenedUrlDisplay.innerHTML = `<a href="${data.short_url}" class="urltext" target="_blank">${data.short_url}</a>`;

                document.getElementById("qrCodeImage").src = data.file_url;
                document.getElementById("qrCodeImage").style.display = "block";
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


