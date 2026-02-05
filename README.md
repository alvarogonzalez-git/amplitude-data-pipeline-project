<div align="center">
  <img src="https://github.com/user-attachments/assets/ab8eec14-a3b5-4d04-9a84-2928e2c12380" alt="Amplitude Logo" width="30%" />

  <h1>Amplitude Analytics Data Pipeline</h1>

  <p>
    A production-ready <strong>ELT pipeline</strong> for extracting data from <a href="https://amplitude.com/docs/apis/analytics/export">Amplitude's API</a> and loading it to <strong>AWS S3</strong>. This data is warehoused in <strong>Snowflake</strong> and <strong>dbt Platform</strong> is used to transform and model the warehoused data to make it analysis-ready.
  </p>
</div>

<hr />

<h2>🚀 Project Architecture</h2>

<p>The pipeline consists of three stages:</p>
<ol>
  <li><strong>Extract & Load with Python 🐍 </strong>
  <ul>
    <li><code>main.py</code>
      <ul>
        <li>Manages the workflow event order and conditional execution logic.</li>
        <li>Initializes <strong>logging handlers</strong> for each function to capture detailed telemetry for each pipeline phase.</li>
      </ul>
    </li>
    <li><code>amplitude_date_range.py</code>
      <ul>
        <li>Calculates <strong>dynamic, relative time window</strong> using Python.</li>
        <li>Supports configurable ingestion (days, weeks, or hours) while ensuring compliance with Amplitude’s format requirements.</li>
      </ul>
    </li>
    <li><code>amplitude_api_call.py</code>
      <ul>
        <li>Handles API authentication and stream-downloading of <strong> .zip</strong> files.</li>
        <li>Implements a <strong>retry mechanism</strong> with specific mapping for various HTTP errors: 400 (4GB limit), 404 (missing data), and 504 (timeout) errors.</li>
      </ul>
    </li>
    <li><code>amplitude_zip_file_extract.py</code>
      <ul>
        <li>Performs <strong>nested decompression</strong>: unzips downloaded .zip file → walks the directory structures → decompresses <strong>.gz</strong> files.</li>
        <li>Uses <strong>tempfile</strong> and <strong>shutil</strong> for memory-efficient, chunked processing of large JSON payloads.</li>
      </ul>
    </li>
    <li><code>amplitude_s3_load.py</code> 
    <ul>
        <li>Authenticates with AWS Boto3 to upload validated JSON files to S3.</li>
        <li>Executes <strong>atomic cleanup</strong>: local files are deleted only after a successful S3 handshake.</li>
      </ul>
    </li>
  </ul>

  <li><strong>Warehousing - Snowflake ❄️</strong>
  <ul>
    <li><i>Coming soon - loading to Snowflake...</i></li>
  </ul>
  <li><strong>Transform with dbt Plaform 🔶</strong>
  <ul>
    <li><i>Coming soon - transformation with dbt...</i></li>
  </ul>
</ol>

<hr>
<h3>Tech Stack</h3>
<ul>
  <li><strong>Language:</strong> Python 3.12+</li>
  <li><strong>Cloud Services:</strong> AWS S3 (Data Lake)</li>
  <li><strong>Data Warehouse:</strong> Snowflake</li>
  <li><strong>Transformation & Testing:</strong> dbt Platform</li>
  <li><strong>Core Libraries:</strong> 
    <code>boto3</code>, <code>requests</code>, <code>python-dotenv</code>, <code>zipfile</code>, <code>gzip</code></li>
  <li><strong>Observability:</strong> Multi-stream timestamp logging for each of the four functions used in the main.py script.</li>
</ul>
<hr />

<h2>📂 Project Structure</h2>

<pre>
├── logs/                   
│   ├── api_call/           # API connection & file download logs
│   ├── date_range/         # Dynamic date time window calculation logs
│   ├── s3_load/            # Upload JSON to AWS S3 logs
│   └── zip_file_extract/   # Decompression nested .zip logs
├── modules/                
│   ├── amplitude_api_call.py
│   ├── amplitude_date_range.py
│   ├── amplitude_s3_load.py
│   └── amplitude_zip_file_extract.py
├── downloaded_data/        # Temp staging for binary .zip files
├── extracted_data/         # Temp staging for decompressed .json files
├── .env                    # Secret Management (API & AWS Keys)
├── main.py                 # Pipeline Orchestrator
├── requirements.txt        # Managed Dependencies
└── README.md
</pre>

<hr />

<h2>🛠️ Setup & Installation</h2>

<h3>1. Clone the repository</h3>
<pre><code>git clone https://github.com/yourusername/amplitude-data-pipeline.git
cd amplitude-data-pipeline</code></pre>

<h3>2. Install Dependencies</h3>
<pre><code>pip install -r requirements.txt</code></pre>

<h3>3. Configure Secrets</h3>
<p>Create a <code>.env</code> file in the root directory. You must provide both Amplitude Analytics and AWS credentials.</p>

<p><strong>File: <code>.env</code></strong></p>
<pre><code># Amplitude Credentials
AMP_API_KEY=your_amplitude_api_key
AMP_SECRET_KEY=your_amplitude_secret_key
</code></pre>

<pre><code># AWS Credentials
AWS_ACCESS_KEY=your_aws_access_key
AWS_SECRET_KEY=your_aws_secret_key
AWS_BUCKET_NAME=your_s3_bucket_name
</code></pre>

<hr />

<h2>🏃 Pipeline Execution</h2>

<p>The pipeline is fully automated. The main.py script includes logic gates to ensure that extraction only begins if the download is successful, and loading only begins if extraction is verified.</p>

<pre><code>python main.py</code></pre>

<h3>Key Resilience Features:</h3>
<ul>
  <li><strong>Stream Processing:</strong> Decompresses data in binary chunks to maintain a low memory footprint, allowing the pipeline to handle files larger than system RAM.</li>
  <li><strong>State Awareness:</strong> If a specific file fails to upload to S3, the pipeline preserves that specific local file while cleaning up successful uploads, preventing data loss.</li>
</ul>

<h3>Troubleshooting Table:</h3>

<table width="100%">
  <thead>
    <tr>
      <th>Status Code</th>
      <th>Log Signal</th>
      <th>System Action</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>400</code></td>
      <td>"File size max exceeded"</td>
      <td>Terminates current window; requires smaller time-delta input.</td>
    </tr>
    <tr>
      <td><code>404</code></td>
      <td>"No data available"</td>
      <td>Graceful exit; logs incident for audit.</td>
    </tr>
    <tr>
      <td><code>504</code></td>
      <td>"Gateway Timeout"</td>
      <td>Auto-retry triggered (up to 3 attempts).</td>
    </tr>
  </tbody>
</table>

<hr />

<h2>⚙️ Orchestration & Deployment</h2>

<p>
  This project is designed to be compatible with containerized orchestration using Docker and Kestra:
</p>

<ul>
  <li><strong>Containerization:</strong> Fully compatible with <strong>Docker</strong> for isolated environment execution.</li>
  <li><strong>Workflow Management:</strong> Ready for integration with <strong>Kestra</strong> or Airflow for visual DAG management and automated scheduling.</li>
  <li><strong>🔒 Security:</strong> All infrastructure configs (<code>.env</code>, <code>docker-compose.yml</code>) are managed via <code>.gitignore</code> to ensure zero exposure of credentials in version history.</li>
</ul>

<hr />

<h2>📄 License</h2>
<p>This project is open source and available under the <a href="LICENSE">MIT License</a>.</p>
