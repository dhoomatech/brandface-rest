from django.template import Template, Context
from django.core.mail import EmailMultiAlternatives


def send_mail_content(mail_type,context,email):
    if mail_type == "first_mail":
        content = """
            <html>
            <body>
                <p>Hello <strong>{{company_name}}</strong>!</p>
                <p>Thank you for choosing Onzitr Products! We're super thrilled to have you onboard.</p>
                <p>Our team is committed to making sure you have a smooth and successful experience with us.</p>
                <p><strong>What’s Next?</strong></p>
                <p>You are the Platform Administrator for the Onzitr Products you have purchased. You can access your organisation’s credentials as follows:</p>
                <ul>
                <li><strong>URL:  </strong>{{url}}</li>
                <li><strong>Phone number:  </strong>{{phone_number}}</li>
                <li><strong>Email:  </strong>{{email}}</li>
                </ul>
                <p>Warmly,<br>
                <strong>The Onzitr Team</strong><br>
                https://marketplace.onzitr.com</p>
            </body>
            </html>
        """
        subject = "Welcome to Onzitr: Your First steps"
    if mail_type == "continue_purchase_mail":
        content = """
            <html>
            <body>
                <p>Hello <strong>{{company_name}}</strong>!</p>
                <p>Thank you for your recent purchase from the Onzitr Marketplace! We're excited to see you expand your toolkit with us.</p>
                <p>We appreciate your continued support and are committed to ensuring you have a seamless experience with your new additions.</p>
                <p>To access your newly purchased items, please visit your portal at: <strong>{{url}}</strong></p>
                <p>We encourage you to take some time to familiarize yourself with these additions. Should you have any questions or require assistance with any of the items in your order, please do not hesitate to contact our support team. We're always here to help!</p>
                <p>Warmly,<br>
                <strong>The Onzitr Team</strong><br>
                https://marketplace.onzitr.com</p>
            </body>
            </html>
        """
        subject = "Your Recent Onzitr Marketplace Order is Ready!"
    elif mail_type == "renewing_mail":
        content = """
            <html>
            <body>
                <p>Hello <strong>Company Name</strong>!</p>
                <p>Thank you for renewing your Onzitr license! We’re grateful for your continued trust and excited to keep supporting your success..</p>
                <p><strong>What’s New?</strong></p>
                <ul>
                <li><strong>Seamless Access:</strong>Your renewed license is active until <strong>[Renewal End Date]</strong>. No interruptions—keep using all features without missing a beat.</li>
                </ul>
                <p><strong>Your Success Matters to Us:?</strong></p>
                <p><strong>Need Help? </strong>Reach our team at [Support Email]</p>
                <p><strong>Feedback? </strong>Tell us how we can improve! Reply to this email or use the [Link].</p>
                <p><strong>Thank you for choosing Onzitr—we’re honored to keep innovating with you! </strong></p>
                <p>Warm regards,<br>
                <strong>The Onzitr Team</strong><br>
                https://marketplace.onzitr.com</p>
            </body>
            </html>
        """
        subject = "Thank You for Renewing! Your Onzitr License Is Ready for What’s Next"
    elif mail_type == "invoice_reminder":
        content = """
            <html>
            <body>
                <p>Hello <strong>Company Name</strong>!</p>
                <p>Thank you for choosing us. We hope you had the best experience while using Onzitr platform.  Your <Product Name> license will be expire on <Date>.</p>
                <p>A new invoice <Invoice Number> is raised for your next billing cycle and is due for payment. </p>
                <p>10000</p>
                <p>Please complete the payment at the earliest for the continuation of our services</p>
                <p>You can also pay using Credit Card / Debit Card / Net Banking / UPI. </p>
                <p>check your invoice in [app link]</p>
                <p>For any queries or discrepancies. Please contact us at <email> </p>
                <p>Warm regards,<br>
                <strong>The Onzitr Team</strong><br>
                https://marketplace.onzitr.com</p>
            </body>
            </html>
        """
        subject = "Reminder: Your Payment Invoice from Onzitr"
    elif mail_type == "password_reset":
        content = """
            <html>
            <body>
                <p>Hello <strong>{{name}}</strong>!</p>
                <p>We received a request to reset the password for your account associated with this email.</p>
                <p>To reset your password, click the button below:</p>
                <p>{{url}}</p>
                <p>If you didn't request this, you can safely ignore this email—your password will remain unchanged.</p>
                <p>For any queries or discrepancies. Please contact us at <email> </p>
                <p>Warm regards,<br>
                <strong>The Onzitr Team</strong><br>
                https://marketplace.onzitr.com</p>
            </body>
            </html>
        """
        subject = "Password Reset Request"

    elif mail_type == "payment_reminder":
        content = """
            <html>
            <body>
                <p>Hello <strong>{{company_name}}</strong>!</p>
                <p>I hope you’re enjoying {{product_name}}! Your current license expires in <strong>{{days_left}}</strong> days on <strong>{{ending_date}}</strong>, and we’d love to ensure uninterrupted access to your tools.</p>
                <strong>Action Needed: </strong><br>
                <p>A new invoice (<strong>#[Invoice Number]</strong>) for your next billing cycle is now due.  </p>
                <strong>Invoice Details: </strong><br>
                <ul>
                <li><strong>Amount Due:</strong>{{price}}.</li>
                <li><strong>Due Date:</strong>{{ending_date}}.</li>
                </ul>
                <strong>Payment Options: </strong><br>
                <p>Credit/Debit Card | Net Banking | UPI </p>
                <strong>Why Renew Now? </strong><br>
                <p><strong>Avoid Interruptions: </strong>Keep your team’s workflow seamless. </p>
                <p><strong>Continued Support: </strong> Maintain access to continued support assistance. </p>
                <strong>Need Help? ? </strong><br>
                <ul>
                <li>Review invoice details or update billing info:<strong>[Portal Link]</strong>.</li>
                <li>Questions? Reply to this email or contact us at <strong>[Support Email]</strong></li>
                </ul>

                <p>We’re here to help!  </p>
                <p>Warm regards,<br>
                <strong>The Onzitr Team</strong><br>
                https://marketplace.onzitr.com</p>
            </body>
            </html>
        """
        subject = "Gentle Reminder: Renew Your Onzitr License Before [Date] "
    elif mail_type == "payment_failed":
        content = """
            <html>
            <body>
                <p>Hello <strong>{{company_name}}</strong>!</p>
                <p>We regret to inform you that your recent payment attempt was unsuccessful</p>
                <p>Kindly retry the transaction at your earliest convenience. If you encounter any issues or need assistance, please don’t hesitate to reach out to us at marketplace.onzitr.com</p>
                <p>Credit/Debit Card | Net Banking | UPI </p>
                <strong>Why Renew Now? </strong><br>
                <p>Thank you for choosing our services.</p>
                <p>Warm regards,<br>
                <strong>The Onzitr Team</strong><br>
                https://marketplace.onzitr.com</p>
            </body>
            </html>
        """
        subject = "Action Required: Payment Unsuccessful"
    elif mail_type == "otp_sending":
        content = """
            <html>
            <body>
                <p>Hi {{user_name}},</strong>!</p>
                <p>Your One-Time Password (OTP) is: <strong>{{otp}}</strong></p>
                <p>Please do not share this code with anyone. If you did not request this OTP, please ignore this email or contact our support team immediately.</p>
                <p>Warm regards,<br>
                <strong>The Onzitr Team</strong><br>
                https://marketplace.onzitr.com</p>
            </body>
            </html>
        """
        subject = "Your One-Time Password (OTP) for Verification"
    elif mail_type == "enquiry":
        content = """
            <html>
            <body>
                <p>Hi Team,</strong>!</p>
                <p>We have received a new enquiry regarding our <strong>{{project_name}}</strong>. Please find the details below:</p>
                <ul>
                <li>Name:<strong>{{name}}</strong>.</li>
                <li>Email ID: <strong>{{email}}</strong></li>
                <li>Phone Number: <strong>{{ph_no}}</strong></li>
                <li>Company Name: <strong>{{company_name}}</strong></li>
                <li>Employee Count: <strong>{{users_count}}</strong></li>
                </ul>
                <p>Please reach out to him to discuss the requirements in more detail and share the next steps.</p>
                <p>Warm regards,<br>
                From marketplace app enquiry form,<br>
                <strong>The Onzitr Team</strong></p>
            </body>
            </html>
        """
        subject = "App Enquiry – Request for Contact Us Card and Lead Collection Form"
    template = Template(content)
    content = template.render(Context(context))
    from_email = "no-reply@yourdomain.com"
    to = [email]
    msg = EmailMultiAlternatives(subject, "", from_email, to)
    msg.attach_alternative(content, "text/html")
    msg.send()
    print("email sent")