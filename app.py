from flask import Flask, Response, render_template_string, request
import matplotlib
matplotlib.use('Agg')  # Set backend to 'Agg' to avoid GUI warnings
import matplotlib.pyplot as plt
import io
import time

app = Flask(__name__)


html_template = """
<!doctype html>
<html lang="en">
<head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Collatz Conjecture</title>
</head>
<body>
    <h1>Collatz Conjecture</h1>
    <form method="POST" class="mb-3">
        <div class ="mb-3">
            <label for="number" class="form-label">Choose a number:</label>
            <input name="number" type="number" placeholder="Enter an integer" required class="form-control">
        </div>
          <button type="submit" class="btn btn-primary" value="start">Submit</button>
    </form>
    {% if number %}
      <img src="{{ url_for('plot_stream', number=number) }}" alt="live plot">
    {% endif %}
    
    <div class="card">
        <div class="card-header">
          About The Collatz Conjecture
        </div>
        <div class="card-body">
          <p class="card-text">Discovered in 1937 by Lothar Collatz, it defines a few simple rules:</p>
          <ul>
            <li>Input a number</li>
            <li>If odd: multiply by 3 and add 1 (3n+1)</li>
            <li>If even: divide by 2</li>
            <li>repeat until number eventually reaches a loop: 1*3+1 = 4, divide by 2 = 2, divide by 2 = 1: repeating in a loop.</li>
          </ul>
        </div>
        <h3>contact me at altdentifier123@gmail.com for any bugs or tips!</h3>
      </div>

</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    number = request.form.get('number') if request.method == 'POST' else None
    return render_template_string(html_template, number=number)

@app.route('/plot_stream')
def plot_stream():
    try:
        start_number = int(request.args.get('number'))
        if start_number <= 0:
            raise ValueError("Number must be a positive integer.")
    except (ValueError, TypeError):
        return "enter a positive integer.", 400

    def generate_plot():
        fig, ax = plt.subplots()
        x_values = [0]  
        y_values = [start_number]  
        z = start_number


        y_max = max(start_number, 100)
        ax.set_ylim(0, y_max)

        for i in range(1, 100):  
            ax.clear()

            if z % 2 == 0:
                z = z // 2
            else: 
                z = (z * 3) + 1

            x_values.append(i)
            y_values.append(z)

            ax.plot(x_values, y_values, color='b')
            ax.set_ylim(0, y_max)
            ax.set_xlim(0, 100)

            # Stream plot frame
            buf = io.BytesIO()
            fig.savefig(buf, format='jpeg')
            buf.seek(0)

            frame = buf.getvalue()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            time.sleep(0.1)  

    return Response(generate_plot(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
