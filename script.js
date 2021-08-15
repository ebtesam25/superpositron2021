console.log('Loading Shopclusive')
  
  const body = document.querySelector("body")
    if(document.getElementById('productTitle')) {
        var button = document.createElement("button");
            button.innerHTML = "10% Pink Tax";
            button.id = "taxButton";
            button.type = "button";
            button.style.backgroundColor = "pink";
            button.style.color = "#800000";
            button.style.borderRadius = "8px";
            button.style.border = "none";
            document.getElementById("priceblock_ourprice").appendChild(button);

            var taxBtn = document.getElementById('priceblock_ourprice');
            taxBtn.addEventListener('click', function() {
                console.log(document.getElementById("priceblock_ourprice").textContent);
            });
            var button = document.createElement("button");
            button.innerHTML = "Shopclusivity Score: 100";
            button.id = "scoreButton";
            button.type = "button";
            button.style.backgroundColor = "pink";
            button.style.borderRadius = 20;
            button.style.fontWeight = "bold";
            button.style.border = "none";
            button.style.borderWidth = 1;
            button.style.color = "#800000";
            document.getElementById("bylineInfo").appendChild(button);

            var scoreBtn = document.getElementById('bylineInfo');
            scoreBtn.addEventListener('click', function() {
                console.log(document.getElementById("bylineInfo").textContent);
            });


            var div = document.createElement("div");
            div.innerHTML = "Cheaper Alternatives";
            div.id = "altProducts";
            div.type = "div";
            div.style.backgroundColor = "pink";
            div.style.color = "#800000";
            div.style.fontWeight = "bold";
            div.style.padding = "5px";
            div.style.borderRadius = "8px";
            div.style.border = "none";
            document.getElementsByClassName("maple-banner")[0].appendChild(div);
            
            
            var i = 0;
            for (i=0; i<5; i++){
                var br = document.createElement("br");
                document.getElementById("altProducts").appendChild(br);
                var product = document.createElement("a");
                product.innerHTML = `Product ${i} - $ ${i}.00`;
                product.id = `suggestedProduct${i}`;
                product.type = "a";
                product.style.fontWeight = "100";
                product.style.color = "#800000";
                product.style.border = "none";
                document.getElementById("altProducts").appendChild(product);
            }
            
    } else {
        console.log("Lost")
    
    }