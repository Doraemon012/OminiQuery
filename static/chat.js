function extractContent(rawData) {
    const regex = /```json([\s\S]*?)```/;
    const match = rawData.match(regex);
    if (match) {
        return match[1].trim();
    } else {
        return rawData; // No content found
    }
}
var md = window.markdownit();

var number_increment = 0;
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("chat-form").addEventListener("submit", function (event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        const data = Object.fromEntries(formData.entries());

        // Append user message to chat
        const chatContainer = document.getElementById("chat-container");
        const chatBox_user = document.createElement("div");
        chatBox_user.classList.add("chat-box-right");
        const chatMessage = document.createElement("div");
        chatMessage.classList.add("chat-message");
        const message = document.createElement("div");
        message.classList.add("message-right");
        const p = document.createElement("p");
        p.textContent = data.messagePerson;
        message.appendChild(p);
        chatMessage.appendChild(message);
        chatBox_user.appendChild(chatMessage);
        chatContainer.appendChild(chatBox_user);

        // Send the message to the backend
        // wait gif (/home/kaku/Downloads/mod-gif.gif)
        const chatBox_temp = document.createElement("div");

        chatBox_temp.classList.add("chat-box-left");
        const responseChatMessage = document.createElement("div");
        responseChatMessage.classList.add("chat-message");
        const responseMessage = document.createElement("div");
        responseMessage.classList.add("message");
        const imgElement = document.createElement("img");
        // codeElement.textContent = responseData.message + " Result: " + responseData.result;
        imgElement.src = "/static/loading.gif";
        imgElement.style.width = "150px";
        imgElement.style.height = "75px";
        imgElement.style.userSelect = "none";
        responseMessage.appendChild(imgElement);
        responseChatMessage.appendChild(responseMessage);
        chatBox_temp.appendChild(responseChatMessage);
        chatContainer.appendChild(chatBox_temp);

        fetch('/chat-message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
            .then(response => response.json())
            .then(responseData => {
                // remove the wait gif
                chatContainer.removeChild(chatBox_temp);


                // Append the server response to the chat
                

                const chatBox_ai = document.createElement("div");
                chatBox_ai.classList.add("chat-box-left");
                const responseChatMessage = document.createElement("div");
                responseChatMessage.classList.add("chat-message");
                const responseMessage = document.createElement("div");
                responseMessage.classList.add("message");
                const codeElement = document.createElement("div");
                codeElement.innerHTML = md.render(responseData.message);
                // result in p tag
                const p = document.createElement("p");
                p.innerHTML = "<br/><b>Result:</b> " + responseData.result;
                codeElement.appendChild(p);

                responseMessage.appendChild(codeElement);
                responseChatMessage.appendChild(responseMessage);
                chatBox_ai.appendChild(responseChatMessage);
                chatContainer.appendChild(chatBox_ai);

                // Create a div for the chart
                const chartDiv = document.createElement("div");

                chartDiv.id = `chart${number_increment}`;
                chartDiv.style.width = "600px";
                chartDiv.style.height = "400px";
                responseMessage.appendChild(chartDiv);

                // Initialize and configure the chart
                const script = document.createElement("script");
                // script.textContent = extractContent(responseData.charts);
                console.log(extractContent(responseData.charts))
                chartDiv.classList.add("chart-style");
                script.textContent =`
                    (function(){
                        var option = ${extractContent(responseData.charts)};
                        
                    const myChart = echarts.init(document.getElementById('chart${number_increment}'));
                        myChart.setOption(option);
                    })();
                    `
                    responseMessage.appendChild(script);

                // } catch (error) {
                //     // console.error('Error parsing chart data:', error);
                //     return;
                // }
                number_increment++;
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    });
});
// print data from http://127.0.0.1:5000/schema


fetch('/schema')
.then(response => {
    if (response.status === 200) {
        return response.json();
    } else if (response.status === 400) {
        window.location.href = '/';
        throw new Error('Bad Request: Redirecting to home');
    } else {
        throw new Error(`Unexpected response status: ${response.status}`);
    }
})
.then(responseData => {
    // if code == 200, else if 400, redirect to /
    const schemaContainer = document.getElementById("schema");

    for (const [tableName, columns] of Object.entries(responseData)) {
        const tableDetails = document.createElement("details");
        const tableSummary = document.createElement("summary");
        tableSummary.textContent = tableName;
        tableDetails.appendChild(tableSummary);

        columns.forEach(columnName => {
            const columnText = document.createElement("p");
            columnText.textContent = columnName;
            tableDetails.appendChild(columnText);
        });

        schemaContainer.appendChild(tableDetails);
    }
})
.catch((error) => {
    console.error('Error:', error);
});
