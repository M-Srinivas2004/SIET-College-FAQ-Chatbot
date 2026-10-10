const chatWindow = document.getElementById('chatWindow');
const chatForm = document.getElementById('chatForm');
const userInput = document.getElementById('userInput');
const quickButtons = document.querySelectorAll('.chip');

const faq = {
  admissions: 'Admissions usually require a completed application, academic transcripts, ID proof, and relevant entrance exam scores if applicable. Please check the specific program deadlines on the official admissions page.',
  scholarship: 'We offer merit scholarships, need-based financial aid, sports scholarships, and special assistance for outstanding students. Students can apply after admission or during the scholarship intake window.',
  courses: 'Popular programs include B.Tech, BBA, B.Sc, MBA, BA, and interdisciplinary courses in AI, design, business, health sciences, and social sciences.',
  campus: 'Campus life includes student clubs, annual events, cultural festivals, sports activities, mentor support, and career development workshops.',
  fees: 'Tuition and fee structures vary by program. Students can contact the admissions office for the latest fee details and installment plans.',
  placement: 'The college supports student placements through training, mock interviews, resume guidance, internship opportunities, and campus recruitment drives.',
  hostel: 'Hostel accommodation is available for eligible students with facilities such as furnished rooms, Wi-Fi, meals, and security support.',
  contact: 'You can contact admissions, student support, or the academic office through the main information desk or official college portal.',
  default: 'I can help with admissions, scholarships, courses, placements, campus life, hostel facilities, and general student support. Ask me anything about the college.'
};

function addMessage(text, isUser) {
  const message = document.createElement('div');
  message.className = `message ${isUser ? 'user' : 'bot'}`;

  if (!isUser) {
    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    avatar.textContent = 'C';
    message.appendChild(avatar);
  }

  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.textContent = text;
  message.appendChild(bubble);

  chatWindow.appendChild(message);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

function getBotReply(message) {
  const normalized = message.toLowerCase();

  if (normalized.includes('admission') || normalized.includes('apply') || normalized.includes('deadline')) {
    return faq.admissions;
  }

  if (normalized.includes('scholarship') || normalized.includes('fee') || normalized.includes('financial aid')) {
    return faq.scholarship;
  }

  if (normalized.includes('course') || normalized.includes('program') || normalized.includes('study')) {
    return faq.courses;
  }

  if (normalized.includes('campus') || normalized.includes('club') || normalized.includes('event') || normalized.includes('life')) {
    return faq.campus;
  }

  if (normalized.includes('placement') || normalized.includes('job') || normalized.includes('career')) {
    return faq.placement;
  }

  if (normalized.includes('hostel') || normalized.includes('accommodation') || normalized.includes('room')) {
    return faq.hostel;
  }

  if (normalized.includes('contact') || normalized.includes('help') || normalized.includes('support')) {
    return faq.contact;
  }

  return faq.default;
}

function triggerReply(rawMessage) {
  const message = rawMessage.trim();
  if (!message) return;

  addMessage(message, true);

  setTimeout(() => {
    const response = getBotReply(message);
    addMessage(response, false);
  }, 500);
}

chatForm.addEventListener('submit', (event) => {
  event.preventDefault();
  const value = userInput.value.trim();
  if (!value) return;

  triggerReply(value);
  userInput.value = '';
  userInput.focus();
});

quickButtons.forEach((button) => {
  button.addEventListener('click', () => {
    const message = button.dataset.message;
    triggerReply(message);
  });
});
