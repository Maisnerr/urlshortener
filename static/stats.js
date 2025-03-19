const localurl = "https://linkly.fun";
const form = document.getElementById('urlForm');

const statheader = document.getElementById("statheader");
const statimg = document.getElementById("statimg");
const statshort = document.getElementById("statshort");
const statlong = document.getElementById("statlong");
const statclicks = document.getElementById("statclicks");
const statdate = document.getElementById("statdate");

form.addEventListener('submit', async (event) => {
    event.preventDefault();  // Prevent form from submitting traditionally

    const shortUrl = urlInput.value.trim();

    if (!shortUrl) {
        alert("Please enter a URL");
        return;
    }

    // Send a GET request to Flask backend
    try {
        const response = await fetch(localurl + '/stats/' + shortUrl, {
            method: 'GET',  // GET request to retrieve stats
        });

        // Check if the response is successful (status 200)
        if (response.ok) {
            const data = await response.json();
            // Now you have the data, you can use it

            if (data.short_url) {
                showStats(data.short_url,data.long_url,data.clicks,data.date,data.img_url);
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

function showStats(short_url, long_url, clicks, date, img_url){
    statshort.innerHTML = "Short URL: linkly.fun/"+short_url;
    statlong.innerHTML = "Long URL: "+long_url;
    statclicks.innerHTML = "Clicks: "+clicks;
    statdate.innerHTML = "Date: "+date;

    statheader.innerHTML = "/"+short_url;
    statimg.src = img_url;
}