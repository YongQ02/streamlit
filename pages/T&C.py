import streamlit as st

st.title("Terms & Condition")

"""# 1. User Consent and Privacy:
Informed Consent: \n 
Before using the bot, the user should be informed about the purpose of the bot, how their data will be used, and their rights (such as data privacy and the option to stop using the service at any time). This is crucial for user trust and transparency.\n 
Confidentiality: The bot should respect user privacy by ensuring that sensitive information (like health details or personal struggles) is not shared or stored improperly. Ideally, the bot should not store conversations unless absolutely necessary, and it should comply with applicable data protection laws (e.g., GDPR, HIPAA).\n 
Data Security: The bot’s platform should be secure, with encryption in place to protect sensitive data, especially if the user shares personal experiences related to their mental health.

# 2. Clear Limitations and Disclaimers:\n 
Non-Diagnosis Disclaimer: \n 

The bot should clearly state that it cannot diagnose or provide specific medical advice. It can offer general mental health guidance or provide emotional support, but it should always recommend that users consult with licensed professionals for proper diagnosis or treatment.\n 
Example: "I am here to listen and provide support, but I am not a licensed therapist. If you are experiencing distress or need medical help, please consider reaching out to a healthcare provider."\n 
Emergency Disclaimer: The bot should display an emergency disclaimer in case the user is in immediate danger, such as if they express thoughts of self-harm or suicide. The bot should then guide them toward appropriate emergency resources (e.g., a suicide prevention hotline or emergency services).\n 
Example: "If you're having thoughts of harming yourself or others, please reach out to someone immediately. You can contact a crisis hotline at 
[ 03-2780 6803 // 03-7772 2899 // 011-3338 8567 ] 
or go to your nearest emergency room."

# 3. Empathy and Tone:\n 
Supportive Language:\n  The bot should use empathetic, non-judgmental, and understanding language to ensure that the user feels heard and valued. The tone should be warm, validating, and comforting, especially if the user expresses difficult emotions.\n 
Example: "I hear you, and it sounds like you're going through a tough time right now. I'm really glad you reached out, and I’m here to listen."\n 
Non-Triggering: The bot should be designed to avoid triggering language that could worsen the user’s mental state. It should be mindful of the language around sensitive topics like trauma, self-harm, and mental illness.

# 4. Active Listening and Engagement:\n 
Open-Ended Questions: \n The bot should ask open-ended questions that encourage the user to talk more freely about their feelings or experiences. It should allow users to express themselves fully without making them feel rushed.\n 
Example: "Can you tell me more about what you've been going through?"\n 
Empathetic Responses: \n After receiving a user’s message, the bot should provide responses that acknowledge the user’s feelings and offer support or resources. The bot might use prompts like:\n 
"It sounds like you're feeling really overwhelmed. I'm really sorry you're going through that."
"It’s okay to feel this way. It might help to talk more about what’s been on your mind."

# 5. Crisis Management and Referral to Professionals:\n 
Identifying Crisis Signals:\n  The bot should be programmed to recognize signals of distress, such as mentions of self-harm, suicide, or severe emotional pain. If detected, the bot should intervene by immediately directing the user to appropriate crisis resources, such as:\n 
Suicide prevention hotlines\n 
Text lines or chat services for mental health\n 
Emergency contacts or medical professionals\n 
Referral to Professionals: Even if a user is not in crisis, the bot should encourage users to seek help from a licensed therapist, counselor, or healthcare provider if they show signs of ongoing distress.\n 
Example: "Talking to a counselor or therapist might really help you work through these feelings. Would you like some help finding a professional?"

# 6. Limitations on the Scope of Assistance:\n 
Providing Emotional Support, Not Therapy: \n The bot should focus on offering emotional support (such as validating feelings, encouraging healthy coping strategies, or providing mental health resources) but should avoid offering any form of psychotherapy, diagnosis, or treatment.\n 
Resource Navigation: The bot can direct users to mental health resources, such as online therapy platforms, self-help articles, or guided mindfulness exercises, but it should never offer detailed psychological advice.


# 7. Monitoring and Feedback:\n 
Periodic Check-ins: \n To keep users engaged and ensure they’re not feeling neglected, the bot can ask regular check-ins, such as:\n 
"How are you feeling today?"\n 
"Have things improved since we last spoke?"\n 
Feedback Mechanism: The bot should have an option for users to provide feedback on their experience with the bot. This feedback can be used to improve the bot’s functionality and support.

# 8. Compliance with Ethical Guidelines:\n 
Ethical AI Use: \n The bot should be designed in compliance with ethical standards for AI, ensuring that it promotes mental well-being and doesn’t inadvertently cause harm. This includes regularly updating the bot to avoid biases, improve conversational quality, and adjust to new psychological research.\n 
Respect for Cultural Sensitivity: Mental health issues are experienced differently across cultures and communities. The bot should be mindful of cultural, social, and language differences to ensure it provides inclusive and respectful support.

# 9. Continuous Monitoring and Updates:\n 
Ongoing Content Review:\n  Mental health guidelines and resources evolve over time, so the bot should be regularly updated to reflect current best practices, new research, and user feedback.\n 
Human Backup: The bot should offer an option for users to escalate their conversation to a human counselor or mental health professional if the user feels the need for more personalized support.

By using this service, you agree to the following terms:\n 
Privacy:\n  Your personal data will be kept confidential and will not be shared without your consent, except when required by law.\n 
Non-Diagnostic: The bot cannot diagnose any mental health conditions or offer professional therapy. It is for informational and emotional support purposes only.\n 
Emergency Situations: If you are experiencing a mental health crisis or need immediate help, you should reach out to a licensed professional or emergency service.\n 
Limited Scope: The bot is not a replacement for therapy, medical advice, or treatment. If you need ongoing support, we encourage you to seek help from a qualified mental health provider.
"""

if 'read' not in st.session_state:
    st.session_state.read = False

if st.button('I have read the Terms & Condition'):
    st.session_state.read = True
    st.success("You can now access the chat")