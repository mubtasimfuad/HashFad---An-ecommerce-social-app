
style = '''<style>
.main_image{grid-area: overflow;}

    .main_text{
    grid-area:overflow;
    color: white;
    margin: auto auto auto 5%;
    font-size: 2rem;
    line-height: 3rem;} 
    .main{
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows:1fr; 
    grid-template-areas: "overflow";
    }
</style>
'''



def format_html(data):
        body_html = f'''
                <html>
                    <head>
                        <title>Happy Birthday Wishing - Chamaparan Now </title>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <!-- Google Fonts -->
                        <link href="https://fonts.googleapis.com/css?family=Pacifico&display=swap" rel="stylesheet">
                        <!-- My Stylesheet -->
                        <link rel="stylesheet" href="style.css">
                        {style}
                    </head>

                <div class="main">
                            
                    <div class="main_image" >
                        <img src="https://media.istockphoto.com/photos/birthday-cupcake-with-balloons-picture-id1250275937?b=1&k=20&m=1250275937&s=612x612&w=0&h=GbuvMVON9sACegGZIXYnegOE7SJll1u9BQGtxT9_fWA=" style="width:100%; height:auto">
                    </div>

                    <div class="main_text" style="color:blue;" > 
                            <p>Happy Birthday</p>
                            <h2>{data['name']}</h2>
                            <p >May all your dreams <br> come true and <br> May God crown you <br> with all the success<br>
                in life. Happy birthday! <br>From- HashFad Family</p>
                    </div>  
                </div>
                
                
                    <!-- JavaScript Page -->
                    <script src="function.js" type="text/javascript"></script>
                </body>
                </html>
                            '''
        return body_html

