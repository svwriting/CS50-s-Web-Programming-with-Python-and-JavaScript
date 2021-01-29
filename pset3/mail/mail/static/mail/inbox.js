document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', compose_email);

    // By default, load the inbox
    load_mailbox('inbox');
});

function compose_email() {

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
    document.querySelector('#email-view').style.display = 'none';

    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
    // // set default
    // document.querySelector('#compose-recipients').value = 'testUser_1@mailmail.com';
    // document.querySelector('#compose-subject').value = 'Meeting time';
    // document.querySelector('#compose-body').value = 'How about we meet tomorrow at 3pm?';

    // Add Event(s)
    document.querySelector('#compose-form').onsubmit = () => {
        fetch('/emails', {
                method: 'POST',
                body: JSON.stringify({
                    recipients: document.querySelector('#compose-recipients').value,
                    subject: document.querySelector('#compose-subject').value,
                    body: document.querySelector('#compose-body').value + '\n'
                })
            }).then(response => response.json())
            .then(result => {
                // Print result
                console.log(result);
                load_mailbox('sent');
            }).catch(error => {
                console.log('Error:', error);
            });
        return false;
    }

function load_mailbox(mailbox) {

    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'none';

    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    // Show mails
    console.log(mailbox);
    fetch('/emails/' + mailbox)
        .then(response => response.json())
        .then(emails => {
            // Print emails
            console.log(emails);

            // ... do something else with emails ...
            const gap_ = document.createElement('div');
            gap_.style.height = '2px';
            gap_.className = 'gap_';
            for (let i = 0; i < emails.length; i++) {
                const emailPreviewBox_ = document.createElement('div');
                emailPreviewBox_.dataset.emailID = emails[i].id;
                emailPreviewBox_.className = "EmailPreviewBox ";
                if (emails[i].read) {
                    emailPreviewBox_.className += "PreviewRead";
                } else {
                    emailPreviewBox_.className += "PreviewUnread";
                }
                const email_sender = document.createElement('div');
                email_sender.className = 'emails_sender';
                email_sender.innerHTML += `From: ${ emails[i].sender }`;
                emailPreviewBox_.append(email_sender);
                const email_subject = document.createElement('div');
                email_subject.className = 'emails_subject';
                email_subject.innerHTML += `Subject: ${ emails[i].subject }`;
                emailPreviewBox_.append(email_subject);
                const email_timestamp = document.createElement('div');
                email_timestamp.className = 'emails_timestamp';
                email_timestamp.innerHTML += `${ emails[i].timestamp }`;
                emailPreviewBox_.append(email_timestamp);
                emailPreviewBox_.addEventListener('click', () => {
                    load_mail(emailPreviewBox_.dataset.emailID);
                });
                document.querySelector('#emails-view').append(emailPreviewBox_);
                document.querySelector('#emails-view').append(gap_.cloneNode(true));
            }
        });
}

function load_mail(mailid) {

    // Show the mail and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'block';

    // Show the mail
    console.log(mailid);
    fetch('/emails/' + mailid)
        .then(response => response.json())
        .then(email => {
            // Print email
            console.log(email);
            // ... do something else with email ...
            if (!email.read) {
                fetch('/emails/' + mailid, {
                    method: 'PUT',
                    body: JSON.stringify({
                        read: true
                    })
                });
                console.log(`(${mailid}).read=true`);
            }
            // render email-view ...
            document.querySelector('.email_subject').innerHTML = `${email.subject}`;
            document.querySelector('.email_timestamp').innerHTML = `${email.timestamp}`;
            document.querySelector('.email_sender').innerHTML = `${email.sender}`;
            document.querySelector('.email_recipients').innerHTML = ` ${email.recipients}`;
            document.querySelector('.email_body').innerHTML = `${email.body}`;
            if (email.sender === document.querySelector('#logging_email').innerHTML) {
                document.querySelector('#archive_btn').style.display = 'none';
                document.querySelector('#reply_btn').style.display = 'none';
            } else {
                document.querySelector('#reply_btn').style.display = 'block';
                document.querySelector('#reply_btn').onclick = () => {
                    compose_email();
                    document.querySelector('#compose-recipients').value = `${email.sender}`;
                    if (email.subject.startsWith("Re: ")) {
                        document.querySelector('#compose-subject').value = `${email.subject}`;
                    } else {
                        document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
                    }
                    document.querySelector('#compose-body').value = "\n\n-------------------------------------------------------------------\n";
                    document.querySelector('#compose-body').value += `On ${email.timestamp} ${email.sender} wrote:\n>>>\n`;
                    document.querySelector('#compose-body').value += `${email.body}`;
                };
                document.querySelector('#archive_btn').style.display = 'block';
                document.querySelector('#archive_btn').dataset.archived = email.archived;
                document.querySelector('#archive_btn').onclick = () => {
                    let archived_ = 'true' === document.querySelector('#archive_btn').dataset.archived;
                    archived_ = !archived_;
                    fetch('/emails/' + mailid, {
                        method: 'PUT',
                        body: JSON.stringify({
                            archived: archived_
                        })
                    }).then(() => {
                        load_mailbox('inbox');
                    });
                    //document.querySelector('#archive_btn').dataset.archived = archived_;
                    //archbtn_cc(archived_);
                };
                archbtn_cc(email.archived)
            }
        });
}

function archbtn_cc(archived) {
    if (archived) {
        document.querySelector('#archive_btn').style.color = 'white';
        document.querySelector('#archive_btn').style.backgroundColor = '#007bff';
    } else {
        document.querySelector('#archive_btn').style.color = '';
        document.querySelector('#archive_btn').style.backgroundColor = '';
    }
}