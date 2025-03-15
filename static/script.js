const form = document.getElementById('urlForm');
const urlInput = document.getElementById('urlInput');
const shortInput = document.getElementById('shortInput');
const shortenedUrlDisplay = document.getElementById('shortenedUrl');

var user = "admin";

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
    event.preventDefault();  // Prevent form from submitting traditionally
        
    const longUrl = urlInput.value.trim();
    const after = shortInput.value.trim();

    if (!longUrl) {
        alert("Please enter a URL");
        return;
    }

    // Send a POST request to Flask backend
    try {
        const response = await fetch('http://192.168.1.138:5000/shorten', {
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

async function appendRow() {
    let table = document.getElementById("myTable");

    let pole = [1,1,1,1,1];
    const len = [1,1,1,1,1];

    let input = []

    for(let i in len){
        mezi = table.insertRow();

        try{
            const response = await fetch("http://192.168.1.138:5000/getdata", {
                method: "POST",
                headers:{
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({amount: i})
            });

            if(response.ok){
                const data = await response.json();
                input = [data.short_url, data.long_url, "", data.clicks, data.date];
            }else{
                console.log(errorData.error);
            }
        } catch (error){
            console.error('Error during request:', error);
        }

        for(let j in pole){
            if(j == 0){
                mezi.insertCell(j).innerHTML = `<div class="firstBox"><a href='http://192.168.1.138:5000/${input[j]}' class="nowrap">http://192.168.1.138:5000/${input[j]}</a><button class="copy" onclick="copyUrl('http://192.168.1.138:5000/${input[j]}')">cau</button></div>`;
            }else if(j == 2){
                mezi.insertCell(j).innerHTML = `<div class="qrImagesDiv"><img src='/static//qrs/${input[0]}.png' alt="QR CODE" width="50px"></div>`;
            }else if(j > 2){
                mezi.insertCell(j).innerHTML = `<p class="aTableDiv nowrap">${input[j]}</p>`; //align do prostred!!!
            }else{
                mezi.insertCell(j).innerHTML = `<p class="nowrap">${input[j]}</p>`; 
            }
        }
    }
}

document.addEventListener("DOMContentLoaded", function () {
    appendRow();
});

// #############################
// AZ BUDE HTTPS UDELAT TO JINAK
// #############################
function copyUrl(link){
    const textArea = document.createElement('textarea');
    textArea.value = link;
    document.body.appendChild(textArea);
    
    textArea.select();

    document.execCommand('copy');
}