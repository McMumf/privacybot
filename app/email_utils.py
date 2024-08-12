
def format_body(ordered_list) -> str:
    """
    Write and format the message body with an ordered list of user details
    """
    return \
        """<html>
        <head>
            <h1 align="center"> CCPA Deletion Request </h1>
        </head>
        <body>
            <p>Hello! <br/>
            I wish to exercise my rights under the California Consumer Privacy Act (CCPA). <br/>
            I request that your business complies with the following requests which are granted to me by the CCPA: <br/>
            <ol>
                <li>Right to Delete</li>
                <li>Right to not sell my information</li>
            </ol>
            </p>

            <p>
            My details are:<br/>
            <ol>
                {code}
            </ol>
            </p>
            <p>
            Let me know if you have any questions.
            </p>
            <br/>
            <p>
            In the case that no email or user name information exists in your records, under the CCPA the above information can only be used for verification purposes and you may not collect it.
            </p>
        </body>
        </html>
        """.format(code=ordered_list)

def format_confirmation_email(sent_result: str) -> str:
    return \
        """<html>
        <head>
            <h1 align="center">PrivacyBot Confirmation</h1>
        </head>
        <body>
            <p>Thank you for using PrivacyBot!</p>

            <p>So, what just happened?</p>
            <ol type="1">
            <li>You filled in the required data fields.</li>
                <ol type="a">
                <li>Data brokers needed to collect additional info to verify your identity and ensure they’re deleting the right person’s data. PrivacyBot only sent the minimum amount of information required for each data broker to delete your info, nothing more.</li>
                </ol>
            <li>Data deletion requests were sent from your email.</li>
                <ol type="a">
                <li>PrivacyBot is essentially a smart email routing tool. You just send CCPA data delete requests en masse right from your own email. PrivacyBot accessed your email through OAuth tokens and ran entirely from your own machine.</li>
                </ol>
            <li>Any replies/next steps will be sent to your inbox.</li>
                <ol type="a">
                <li>Any follow-ups from the companies themselves will go directly back to you. All further communications will be between you and the company, we just helped to kick start the process.</li>
                </ol>
            </ol>
            If you selected a subset of data brokers that require some follow-up, they will be following up with you directly. Some possible responses you may be receiving include:
            <ol type="1">
            <li>The form fill out</li>
                <ol type="a">
                <li>Some companies will respond with a form they want you to fill out, regardless of how much info you included in the email. This may be because email was not one of their accepted methods of CCPA deletion requests, but they will still send you the link to the form you need to fill out, making it easier for you to submit your deletion request.</li>
                <li>E.g “For privacy inquiries, please contact us by filling out the "Privacy Choices and Data Subject Rights" form available at [Link]”</li>
                </ol>
            <li>The confirmation email</li>
                <ol type="a">
                <li>The number of these you will get will vary depending on how many data fields you included in your requests - if you included all of them, odds are you’ll be getting a lot of these. More often than not, these don’t require any response from you and are merely confirming receipt of your request.</li>
                <li>E.g “This will confirm that we have received your request to delete your information from the database.” </li>
                </ol>
            <li>The information ask</li>
                <ol type="a">
                <li>Again depending on how many data fields you included in your request, you may receive a lot or only a few of these responses. These will happen when you did not input enough data into the deletion request, and merely require you to include some additional information. Whether you want to supply that information is up to you, but be assured that companies are legally not allowed to save any of that data they request from you.
                <li>E.g “Please confirm the following additional information about yourself: Your full residential address.”
                </ol>
            </ol>
            Again, thank you for using PrivacyBot! Here’s a link to our Privacy Policy and our <a href="https://privacybot.io/FAQ">FAQ</a> if you have any other questions! <br/>
            </br>
            <h2> Please remove permissions for PrivacyBot from your Gmail account. </h2></br>
            <br/><br/>
            Best,<br/>
            The PrivacyBot Team<br/>

        </body>
        </html>
        """.format(sentresult=sent_result)
