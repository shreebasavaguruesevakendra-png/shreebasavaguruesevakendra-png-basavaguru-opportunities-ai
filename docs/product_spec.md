# Basavaguru Opportunities AI Product Spec

## Vision

Create an AI-powered platform that automatically tracks, collects, organizes, and distributes government opportunities, schemes, scholarships, jobs, admissions, welfare benefits, and public service notifications relevant to Karnataka citizens.

The end goal is to become the most trusted source for students, job seekers, farmers, labourers, women, senior citizens, and the general public.

## Problem

Government information is scattered across hundreds of websites. Citizens often miss scholarships, jobs, labour benefits, pension schemes, farmer subsidies, admission notifications, and welfare schemes.

Most people do not know:

- What they are eligible for
- Last dates
- Required documents
- Application links

## Solution

Build an AI agent that scans government websites every 24 hours and automatically:

1. Detects new notifications
2. Extracts important information
3. Categorizes opportunities
4. Stores them in a database
5. Sends daily updates
6. Answers citizen queries

## Categories

### Students

- SSP Scholarships
- NSP Scholarships
- Minority Scholarships
- SC/ST Scholarships
- Merit Scholarships
- Hostel Admissions
- KCET Updates
- NEET Counselling
- ITI Admissions
- Diploma Admissions
- Degree Admissions
- Nursing Admissions
- Skill Development Programs

### Job Seekers

- KPSC
- SSC
- UPSC
- Railways
- Banking Jobs
- Police Recruitment
- Forest Department
- Village Accountant
- PDO Recruitment
- India Post
- Apprenticeships
- Employment Fairs

### Women

- Gruha Lakshmi
- Shakti Scheme
- SHG Benefits
- Entrepreneurship Schemes
- Widow Assistance
- Maternity Benefits

### Labour Workers

- Labour Card Benefits
- Marriage Assistance
- Education Assistance
- Housing Benefits
- Accident Compensation
- Welfare Board Schemes

### Farmers

- PM-KISAN
- Crop Insurance
- Equipment Subsidies
- Irrigation Subsidies
- Dairy Schemes
- Horticulture Schemes
- Animal Husbandry Schemes

### Senior Citizens

- Old Age Pension
- Healthcare Schemes
- Disability Benefits
- Welfare Programs

### Public Services

- Bus Pass Notifications
- Aadhaar Updates
- PAN Services
- Ration Card Updates
- Voter ID Updates
- Income Certificate Updates
- Caste Certificate Updates

## Data Sources

### Karnataka

- Seva Sindhu
- SSP Karnataka
- KPSC
- KEA
- Karnataka Government Departments

### National

- SSC
- UPSC
- RRB
- National Scholarship Portal
- India Post
- Ministry Portals

## Data Fields

The platform should extract and store:

- Title
- Category
- Audience
- Eligibility
- Benefits
- Documents required
- Last date
- Official link
- Source name
- Source URL
- First seen date
- Last seen date

## Distribution Channels

1. Website dashboard
2. WhatsApp channel
3. Telegram channel
4. Mobile application
5. AI chat assistant

## Technology Phases

### Phase 1

- n8n
- Google Sheets
- OpenAI API
- Telegram Bot

### Phase 2

- PostgreSQL database
- Website dashboard
- WhatsApp integration

### Phase 3

- RAG-based AI assistant
- Mobile application
- Multi-language support

## Revenue Opportunities

- eSeva service leads
- Premium alerts
- Educational admissions
- Scholarship assistance
- Job application assistance
- Government form filling
- Advertising from local institutions

## Execution Plan

1. Build data collection system
2. Create notification database
3. Launch Telegram and WhatsApp alerts
4. Launch website dashboard
5. Launch AI search assistant
6. Expand into full Karnataka Opportunity Platform
