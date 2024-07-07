HTML_CONTENT = """
<!DOCTYPE html>
<html>
<head>
    <title>RFID Reader Web Interface</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        h1, h2 {
            color: #333;
        }
        form {
            margin-bottom: 20px;
        }
        input[type="number"], input[type="text"] {
            padding: 8px;
            font-size: 16px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        input[type="submit"] {
            padding: 10px 20px;
            font-size: 16px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background-color: #45a049;
        }
        #continuous_read_result {
            width: 100%;
            height: 200px;
            padding: 8px;
            font-size: 14px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <h1>RFID Reader Web Interface</h1>
    <h2>Single Read</h2>
    <form action="/single_read">
        Timeout (seconds): <input type="number" name="timeout" value="15"><br><br>
        <input type="submit" value="Read RFID">
    </form>
    <p>Result: <span id="single_read_result"></span></p>

    <h2>Read Specific ID</h2>
    <form action="/specific_read">
        Chip ID: <input type="text" name="chip_id"><br><br>
        <input type="submit" value="Read RFID">
    </form>
    <p>Result: <span id="specific_read_result"></span></p>

    <h2>Continuous Read</h2>
    <form action="/continuous_read">
        Timeout (seconds): <input type="number" name="timeout"><br><br>
        <input type="submit" value="Start Continuous Read">
    </form>
    <p>Results:</p>
    <textarea id="continuous_read_result" rows="10" cols="50"></textarea>

    <script>
        function updateResult(elementId, result) {
            document.getElementById(elementId).innerText = result;
        }

        function updateContinuousResult(result) {
            var textarea = document.getElementById("continuous_read_result");
            textarea.value += result + "\\n";
        }
    </script>
</body>
</html>
"""
