const openFileMenuButton = document.getElementById("openFileMenuButton");
const fileMenu = document.getElementById("fileMenu");
    
openFileMenuButton.addEventListener("click", () => {
    fileMenu.style.display = fileMenu.style.display === "none" ? "block" : "none";
});

const form = document.getElementById("feedbackForm");

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    
    const feedback = document.getElementById("feedback").value;
    const feedbackType = document.getElementById("feedbackType").value;
    const fileName = document.getElementById("fileName").value;
    const fileInfo = document.getElementById("fileInfo").value;
    const fileInput = document.getElementById("file");
    
    const formData = new FormData();

    formData.append("feedback", feedback);
    formData.append("feedbackType", feedbackType);
    if (fileName) {
        formData.append("fileName", fileName);
    }
    if (fileInfo) {
        formData.append("fileInfo", fileInfo);
    }
    if (fileInput.files.length > 0) {
        formData.append("file", fileInput.files[0]);
    }

    try {
        const response = await fetch("/send_feedback", {
            method: "POST",
            body: formData,
        });
    
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || "Error uploading the file");
        }
    
        alert("The feedback has been sent successfully!");
    
        fileMenu.style.display = "none";
    } catch (error) {
        alert(error.message);
    }
});