const localurl = "https://www.linkly.fun"

async function appendRow() {
    let table = document.getElementById("myTable");

    let pole = [1,1,1,1,1];
    let len = [];
    let input = [];

    try{
        const response = await fetch(localurl+"/getlength", {
            method: "POST",
            headers:{
                "Content-Type": "application/json"
            },
            body: JSON.stringify({amount: "1"})
        });

        if(response.ok){
            const data = await response.json();
            len = data.len;
        }else{
            console.log(errorData.error);
        }
    } catch (error){
        console.error('Error during request:', error);
    }

        for(let i in len){
        mezi = table.insertRow();     
        mezi.classList.add("interlight");      

        try{
            const response = await fetch(localurl+"/getdata", {
                method: "POST",
                headers:{
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({amount: i})
            });

            if(response.ok){
                const data = await response.json();
                input = [data.short_url, data.long_url, "", data.clicks, data.date, data.img_url];
            }else{
                console.log(errorData.error);
            }
        } catch (error){
            console.error('Error during request:', error);
        }

        for(let j in pole){
            if(j == 0){
                mezi.insertCell(j).innerHTML = `<div class="firstBox"><a href="${localurl}/${input[j]}" class="nowrap">${localurl}/${input[j]}</a><button class="copy" onclick="copyUrl('${localurl}/${input[j]}')">Copy</button></div>`;
            }else if(j == 2){
                mezi.insertCell(j).innerHTML = `<div class="qrImagesDiv"><img src='${input[5]}' alt="QR CODE" width="50px"></div>`;
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
