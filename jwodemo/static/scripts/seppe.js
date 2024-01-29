document.addEventListener("DOMContentLoaded", function (event) {
    // Find all <p> and <li> elements on the page
    var elements = document.querySelectorAll("p, li");

    // Loop through each element
    for (var i = 0; i < elements.length; i++) {
        var element = elements[i];
        var preserveWord = element.getAttribute("data-preserve");
        var text = element.textContent;

        // Only proceed if the "data-preserve" attribute is not present or is set to "false"
        if (preserveWord !== "true") {
            // Replace instances of "seep coin", "seep", "seppe", "guiseppe", "soup", "soupy", and "seep coins" with the formatted version
            var newText = text.replace(/\b(seep coins?|seep|seppe|guiseppe|soup|soupy)\b/gi, function(match) {
                if (match.toLowerCase() === 'seep coin' || match.toLowerCase() === 'seep coins') {
                    return '<span class="seep-coin-font">' + match + '</span>';
                } else {
                    return '<span class="word-seppe">' + match + '</span>';
                }
            });

            // Update the element if necessary
            if (newText !== text) {
                element.innerHTML = newText;
            }
        }
    }
});

/*

                <p>Here is a normal sentence with the word "seppe".</p>
                <p data-preserve="true">This sentence contains "seppe" and should not be changed.</p>
                <p>Another sentence with the word "seppe".</p>

*/

