const localurl = "https://www.linkly.fun"
// http://192.168.1.138:5000
// https://www.linkly.fun

const form = document.getElementById('urlForm');
const urlInput = document.getElementById('urlInput');
const shortInput = document.getElementById('shortInput');
const shortenedUrlDisplay = document.getElementById('shortenedUrl');
const spinner = document.getElementById("spinner");

var user = "admin";

let gotoUrl = "";

const datum = new Date();
switch(datum.getMonth()){
    case 0:
        var month = "Jan";
        break;
    case 1:
        var month = "Feb";
        break;
    case 2:
        var month = "Mar";
        break;
    case 3:
        var month = "Apr";
        break;
    case 4:
        var month = "May";
        break;
    case 5:
        var month = "Jun";
        break;
    case 6:
        var month = "Jul";
        break;
    case 7:
        var month = "Aug";
        break;
    case 8:
        var month = "Sep";
        break;
    case 9:
        var month = "Oct";
        break;
    case 10:
        var month = "Nov";
        break;
    case 11:
        var month = "Dec";
        break;
}
const date = month+" "+datum.getDate().toString()+" "+datum.getFullYear().toString();

form.addEventListener('submit', async (event) => {
    spinner.style.visibility = "visible";
    event.preventDefault();  // Prevent form from submitting traditionally
        
    const longUrl = urlInput.value.trim();
    const after = "";

    if (!longUrl) {
        alert("Please enter a URL");
        return;
    }

    // Send a POST request to Flask backend
    try {
        const response = await fetch(localurl+'/shorten', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json' // Ensure the Content-Type is set to JSON
            },
            body: JSON.stringify({ long_url: longUrl, after: after, date: date}) // Send the URL as JSON
            
        });

        // Check if the response is OK (status 200-299)
        if (response.ok) {
            const data = await response.json();
            if (data.short_url) {
                shortenedUrlDisplay.innerHTML = `<a href="${data.short_url}" class="urltext outputa" target="_blank"><u>${data.short_url}</u></a>`;

                document.getElementById("qrCodeImage").src = data.img_url;
                document.getElementById("qrCodeImage").style.display = "block";

                document.getElementById("utilsid").style.visibility = "visible";

                document.getElementById("utilid0").href = await data.img_url;
                document.getElementById("utilid0").target = "_blank";
                gotoUrl = data.short_url;
                document.getElementById("utilid2").href = data.img_url;
                setTimeout(() => {
                    spinner.style.visibility = "hidden";
                }, 1000);
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

function copyUrl(link){
    if(link==""){
        link = gotoUrl;
    }

    navigator.clipboard.writeText(link);
}
