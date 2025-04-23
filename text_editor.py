import streamlit as st
import json
import os

def load_text_config():
    """Load the text configuration from a JSON file."""
    if os.path.exists('text_config.json'):
        with open('text_config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "metrics": {
            "title": "Key Performance Indicators",
            "content": "মোট বিক্রয় ৯,৩১৩,৯৮৩ টাকা (১১.৯% বৃদ্ধি), গড় দৈনিক বিক্রয় ১০১,২৩৯ টাকা (১১.৯% বৃদ্ধি), মোট গ্রাহক ১,৬৭৯ জন (২.৮% বৃদ্ধি)। রিটার্ন রেট ৯.২% (-০.৩% হ্রাস)।",
            "advice": "পারফরম্যান্স শক্তিশালী, বিশেষত মোট বিক্রয় এবং দৈনিক বিক্রয়ে ১১.৯% বৃদ্ধি। রিটার্ন রেট কমেছে, যা ভালো সংকেত। গ্রাহক বৃদ্ধির হার আরও বাড়ানোর উপায় খুঁজুন।"
        },
        "sales_trend": {
            "title": "Sales Trend Analysis",
            "content": "জুলাই থেকে অক্টোবর ২০২৩ পর্যন্ত দৈনিক বিক্রয়ে উঠানামা দেখা যাচ্ছে। বিশেষ করে জুলাই এবং সেপ্টেম্বরের শুরুতে পিক সেলস (২০০,০০০+ টাকা) দেখা গেছে। রিটার্ন পরিমাণ খুব কম (সাধারণত ১০,০০০ টাকার নিচে)।",
            "advice": "জুলাই এবং সেপ্টেম্বরের বিক্রয় পিক সময়ের কারণ বিশ্লেষণ করুন। আগস্ট ১২ তারিখে বিক্রয় ৭৫,৩০৩ টাকা। সেপ্টেম্বরের শেষে বিক্রয় বৃদ্ধির কারণ খুঁজে বের করে অন্য সময়ে প্রয়োগ করুন।"
        },
        "order_analysis": {
            "title": "Order Source Analysis",
            "content": "ওয়েবসাইট (৪৩.৬%) আপনার প্রধান অর্ডার সোর্স, এরপর ইন্সটাগ্রাম (২১.৩%), ফেসবুক (১৬.৭%), সরাসরি বিক্রয় (১১.৯%)। Product_18, Product_12, এবং Product_8 সবচেয়ে বেশি বিক্রি হচ্ছে, যথাক্রমে প্রায় ৮৫০,০০০, ৮০০,০০০, এবং ৭৫০,০০০ টাকা।",
            "advice": "ওয়েবসাইট ও ইন্সটাগ্রাম মার্কেটিংয়ে বিনিয়োগ বাড়ান। Product_18, Product_12, এবং Product_8 এর স্টক যথেষ্ট রাখুন এবং এই পণ্যগুলোর প্রচার বাড়ান।"
        },
        "inventory": {
            "title": "Inventory Management Insights",
            "content": "এক্সেসরিজ (৩১০+) ও জ্যাকেট (২৮০+) ক্যাটাগরিতে সবচেয়ে বেশি আইটেম স্টকে আছে। দ্বিতীয় গ্রাফে দেখা যায়, টি-শার্ট এবং শার্ট বেশি বিক্রি হচ্ছে (৩M+ ও ২M+ টাকা), কিন্তু তুলনামূলকভাবে কম স্টক (২৪৫ ও ২৭০ আইটেম) আছে।",
            "advice": "এক্সেসরিজের উচ্চ স্টক (৩১০+) হ্রাস করুন কারণ এর বিক্রয় তুলনামূলকভাবে কম (১M টাকার কম)। টি-শার্ট (উচ্চ বিক্রয়, কম স্টক) এর ইনভেন্টরি বাড়ান। ইনভেন্টরি ও বিক্রয় অনুপাত অপ্টিমাইজ করুন।"
        },
        "category": {
            "title": "Category Performance Review",
            "content": "টি-শার্ট ক্যাটাগরি সর্বাধিক আয় (২.৮M+ টাকা, মোট বিক্রয়ের ৩০.৬%) করছে। এরপর শার্ট (২.৪M টাকা, ২৫.৮%), জিন্স (২.১M টাকা, ২২.৮%), জ্যাকেট (১.২M টাকা, ১৩.৩%), এবং এক্সেসরিজ (৭০০K টাকা, ৭.৪%)।",
            "advice": "টি-শার্ট ও শার্ট ক্যাটাগরিতে নতুন পণ্য যোগ করে এই সেগমেন্টকে আরও শক্তিশালী করুন। এক্সেসরিজ ক্যাটাগরির বিক্রয় বাড়াতে ক্রস-সেলিং কৌশল অবলম্বন করুন।"
        },
        "profitability": {
            "title": "Profitability Assessment",
            "content": "টি-শার্ট সবচেয়ে বেশি আয় (২.৮M+ টাকা) ও লাভ (৮৫০K টাকা) দিচ্ছে। জিন্স আয় ২.১M+ টাকা এবং লাভ ৭৫০K টাকা। মোট ৫টি ক্যাটাগরিতে, আয়ের তুলনায় লাভের হার ২৫-৩০% এর মধ্যে।",
            "advice": "টি-শার্ট ও জিন্সের লাভজনকতা বজায় রাখুন। এক্সেসরিজ ও জ্যাকেটের লাভের হার বাড়াতে খরচ কমানোর উপায় খুঁজুন বা প্রিমিয়াম লাইন চালু করুন।"
        },
        "customer_insights": {
            "title": "Customer Behavior Analysis",
            "content": "জুলাই'২৩ থেকে অক্টোবর'২৩ পর্যন্ত দেখা যায় আগস্টে সর্বাধিক ৬০০ জন নতুন গ্রাহক এসেছিল, যা অক্টোবরে কমে ৫০০ এর কাছাকাছি হয়েছে। গ্রাহক প্রতি গড় খরচ জুলাই ও আগস্টে ৬১৫০ টাকা, সেপ্টেম্বরে কমে ৫৭৫০ টাকা, অক্টোবরে বেড়ে ৬০৩০ টাকা।",
            "advice": "আগস্টের গ্রাহক সংখ্যা বৃদ্ধির কারণ অনুসন্ধান করুন (প্রমোশন/ইভেন্ট?)। সেপ্টেম্বরে গড় অর্ডার ভ্যালু কমার কারণ বিশ্লেষণ করুন। অক্টোবরে পুনরায় বৃদ্ধির কৌশল অন্য মাসেও প্রয়োগ করুন।"
        },
        "growth": {
            "title": "Growth and Value Analysis",
            "content": "জুলাই'২৩ থেকে অক্টোবর'২৩ পর্যন্ত গ্রাহক সংখ্যা জুলাইয়ে প্রায় ১০০ থেকে আগস্টে ৬০০ এ বৃদ্ধি পেয়েছে, তারপর ধীরে ধীরে কমেছে। গ্রাহক প্রতি গড় খরচ জুলাই-আগস্টে ৬১৫০ টাকা, সেপ্টেম্বরে কমে ৫৭৫০ টাকা, অক্টোবরে আবার বেড়েছে।",
            "advice": "আগস্টের বৃদ্ধির কৌশল চিহ্নিত করে বাকি মাসগুলোতেও প্রয়োগ করুন। সেপ্টেম্বরে গ্রাহক প্রতি খরচ কমার কারণ খুঁজুন। কাস্টমার লটিং প্রোগ্রাম চালু করে গ্রাহকদের ধরে রাখুন এবং তাদের খরচ বাড়ান।"
        }
    }

def save_text_config(config):
    """Save the text configuration to a JSON file."""
    with open('text_config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

def main():
    st.set_page_config(page_title="Text Editor", layout="wide")
    
    st.title("Dashboard Text Editor")
    st.write("Edit the text content for your dashboard here. Changes will be saved automatically.")
    
    # Load the current configuration
    text_config = load_text_config()
    
    # Create tabs for each section
    tabs = st.tabs(list(text_config.keys()))
    
    # Create editors for each section
    for i, (section, content) in enumerate(text_config.items()):
        with tabs[i]:
            st.subheader(section.replace('_', ' ').title())
            
            # Title editor
            new_title = st.text_input("Title", value=content['title'], key=f"{section}_title")
            
            # Content editor
            st.write("Content")
            new_content = st.text_area("", value=content['content'], height=150, key=f"{section}_content")
            
            # Advice editor
            st.write("Advice")
            new_advice = st.text_area("", value=content['advice'], height=150, key=f"{section}_advice")
            
            # Update the configuration if any changes were made
            if (new_title != content['title'] or 
                new_content != content['content'] or 
                new_advice != content['advice']):
                text_config[section] = {
                    'title': new_title,
                    'content': new_content,
                    'advice': new_advice
                }
                save_text_config(text_config)
                st.success("Changes saved!")

if __name__ == "__main__":
    main() 