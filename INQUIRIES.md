# Enquiries

Build with `python3 build.py`. For a local preview with a working inbox, run
`node demo.mjs` with Node 22.13+ and visit http://127.0.0.1:8765/.
The demo stores enquiries in SQLite under the system temporary directory,
in `habits-demka-malinka/inquiries.sqlite`. Set `HABITS_DEMO_DIR` to a private
directory outside the checkout for longer retention. Set `PORT` to change the port.
The demo makes no email deliveries. A plain static server serves the pages but
requires a separate backend for POST /api/inquiries.

## Cloudflare configuration for launch

Serve `dist` with Pages Functions from the repository root.
Bind a D1 database as `INQUIRIES`; initialize it with `inquiry-schema.sql`.
For Workers with static assets, use `worker.mjs` as the Worker entry point,
bind `dist/` as `ASSETS` and route `/api/*` to the Worker first.
The Worker uses the same D1 binding and handles form submissions itself.

Each accepted enquiry is stored before success is shown. The D1 console provides
access to the inbox for authorized operators. To enable email notifications,
set the `RESEND_API_KEY` secret and `INQUIRY_FROM` to a verified sending
address. Notifications go to `manager@herbits.lt`, with the visitor as Reply-To.
Rows with `notified = 0` are available for manual follow-up if delivery
is disabled or fails. The form always displays the manager's direct email.
