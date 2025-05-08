import tkinter as tk
from tkinter import ttk, messagebox
from db import (login_user, register_user, save_single_prediction, save_recommendation_prediction, get_user_predictions)
from model import predict_single_stock, predict_all_stocks, STOCKS
import uuid
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
import numpy as np 
from PIL import Image, ImageTk
   
class StockApp: 
    def __init__(self, root): 
        self.root = root
        self.root.title("Stock Prediction System") 
        self.root.geometry("1000x750")  # Increased size for better layout
        
        # Define color scheme
        self.colors = {
            'primary': '#2c3e50',      # Dark blue-gray
            'secondary': '#3498db',    # Blue
            'accent': '#2ecc71',       # Green
            'warning': '#e74c3c',      # Red
            'light': '#ecf0f1',        # Light gray
            'dark': '#34495e',         # Darker blue-gray
            'profit': '#27ae60',       # Dark green
            'loss': '#c0392b',         # Dark red
            'background': '#f9f9f9'    # Off-white
        }
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure ttk styles
        self.style.configure('TButton', 
                             font=('Helvetica', 11),
                             background=self.colors['secondary'],
                             foreground='white')
        
        self.style.configure('Primary.TButton', 
                             font=('Helvetica', 12, 'bold'),
                             background=self.colors['primary'],
                             foreground='white')
        
        self.style.configure('Success.TButton', 
                             font=('Helvetica', 12, 'bold'),
                             background=self.colors['accent'],
                             foreground='white')
        
        self.style.configure('TEntry', 
                             fieldbackground=self.colors['light'])
        
        self.style.configure('TCombobox', 
                             fieldbackground=self.colors['light'])
        
        self.style.configure('Treeview', 
                             background=self.colors['light'],
                             fieldbackground=self.colors['light'],
                             foreground=self.colors['dark'])
        
        self.style.configure('Treeview.Heading', 
                             font=('Helvetica', 10, 'bold'),
                             background=self.colors['primary'],
                             foreground=self.colors['light'])
        
        # Create and set background
        self.root.configure(bg=self.colors['background'])
        
        # Initialize user variable
        self.current_user = None
        
        # Start with login screen
        self.show_login()
    
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_header(self, title, show_back=True):
        """Create a standardized header for all screens"""
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header_frame.pack(fill=tk.X)
        
        # Make sure the header has a fixed height
        header_frame.pack_propagate(False)
        
        # Add app title
        title_label = tk.Label(header_frame, 
                              text=title,
                              font=('Helvetica', 22, 'bold'),
                              fg=self.colors['light'],
                              bg=self.colors['primary'])
        title_label.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Add back button if needed
        if show_back and self.current_user:
            back_btn = tk.Button(header_frame, 
                                text="← Back",
                                font=('Helvetica', 12),
                                fg=self.colors['light'],
                                bg=self.colors['primary'],
                                bd=0,
                                activebackground=self.colors['dark'],
                                activeforeground=self.colors['light'],
                                cursor="hand2",
                                command=self.show_dashboard)
            back_btn.pack(side=tk.RIGHT, padx=20, pady=15)
            
        return header_frame
    
    def create_fancy_button(self, parent, text, command, color=None, width=20, height=2, font_size=14, icon=None):
        """Create a stylized button with hover effect"""
        if color is None:
            color = self.colors['secondary']
        
        button_frame = tk.Frame(parent, bg=self.colors['background'])
        
        def on_enter(e):
            button['background'] = self.lighten_color(color)
            
        def on_leave(e):
            button['background'] = color
        
        button = tk.Button(button_frame, 
                          text=text,
                          font=('Helvetica', font_size, 'bold'),
                          bg=color,
                          fg='white',
                          width=width,
                          height=height,
                          relief=tk.RAISED,
                          bd=0,
                          command=command,
                          cursor="hand2")
        
        button.pack(padx=5, pady=5)
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
        return button_frame
    
    def lighten_color(self, hex_color, factor=0.1):
        """Lighten a hex color by a factor"""
        # Convert hex to RGB
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Lighten
        r = min(255, int(r + (255 - r) * factor))
        g = min(255, int(g + (255 - g) * factor))
        b = min(255, int(b + (255 - b) * factor))
        
        # Convert back to hex
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def create_entry_field(self, parent, label_text, show=None, width=30):
        """Create a standardized entry field"""
        frame = tk.Frame(parent, bg=self.colors['background'])
        
        label = tk.Label(frame, 
                        text=label_text,
                        font=('Helvetica', 12),
                        bg=self.colors['background'],
                        fg=self.colors['dark'])
        label.pack(anchor='w', padx=5, pady=(5, 0))
        
        entry = tk.Entry(frame, 
                        font=('Helvetica', 11),
                        bd=0,
                        relief=tk.SOLID,
                        highlightthickness=1,
                        highlightbackground=self.colors['secondary'],
                        highlightcolor=self.colors['accent'],
                        width=width)
        
        if show:
            entry.config(show=show)
            
        entry.pack(fill=tk.X, padx=5, pady=(2, 5), ipady=8)
        
        return frame, entry
    
    # Authentication Screens
    def show_login(self):
        self.clear_frame()
        self.create_header("AI-Based Stock Market Investment Advisor", show_back=False)
        
        main_frame = tk.Frame(self.root, bg=self.colors['background'])
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Create a card-like container
        login_frame = tk.Frame(main_frame, 
                            bg='white',
                            bd=0,
                            relief=tk.SOLID,
                            highlightthickness=1,
                            highlightbackground=self.colors['light'])
        login_frame.pack(expand=True, fill=tk.BOTH, padx=100, pady=50)
        
        # Logo/Title
        tk.Label(login_frame, 
                text="Login to Your Account",
                font=('Helvetica', 20, 'bold'),
                bg='white',
                fg=self.colors['primary']).pack(pady=(40, 20))
        
        # Username field
        username_frame, self.username_entry = self.create_entry_field(login_frame, "Username", width=40)
        username_frame.pack(pady=10, padx=50, fill=tk.X)
        
        # Password field
        password_frame, self.password_entry = self.create_entry_field(login_frame, "Password", show="*", width=40)
        password_frame.pack(pady=10, padx=50, fill=tk.X)
        
        # Show password checkbox
        show_password_frame = tk.Frame(login_frame, bg='white')
        show_password_frame.pack(padx=50, fill=tk.X, anchor='w')
        
        self.show_password_var = tk.BooleanVar()
        show_password_checkbox = tk.Checkbutton(
            show_password_frame,
            text="Show password",
            variable=self.show_password_var,
            onvalue=True,
            offvalue=False,
            bg='white',
            fg=self.colors['dark'],
            selectcolor=self.colors['light'],
            activebackground='white',
            command=self.toggle_password_visibility
        )
        show_password_checkbox.pack(anchor='w', pady=(0, 10))
        
        # Buttons
        button_frame = tk.Frame(login_frame, bg='white')
        button_frame.pack(pady=20)
        
        login_btn = self.create_fancy_button(button_frame, "Login", self.handle_login, self.colors['accent'])
        login_btn.pack(side=tk.LEFT, padx=10)
        
        register_btn = self.create_fancy_button(button_frame, "Register", self.show_register, self.colors['secondary'])
        register_btn.pack(side=tk.LEFT, padx=10)
        
        # Footer
        '''tk.Label(login_frame, 
                text="© 2025 Stock Prediction System",
                font=('Helvetica', 10),
                bg='white',
                fg=self.colors['dark']).pack(side=tk.BOTTOM, pady=20)'''

    def toggle_password_visibility(self):
        """Toggle password field between showing characters and hiding them"""
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def show_register(self):
        self.clear_frame()
        self.create_header("Create New Account", show_back=False)
        
        main_frame = tk.Frame(self.root, bg=self.colors['background'])
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Create a card-like container
        register_frame = tk.Frame(main_frame, 
                                 bg='white',
                                 bd=0,
                                 relief=tk.SOLID,
                                 highlightthickness=1,
                                 highlightbackground=self.colors['light'])
        register_frame.pack(expand=True, fill=tk.BOTH, padx=80, pady=30)
        
        # Title
        tk.Label(register_frame, 
                text="Create a New Account",
                font=('Helvetica', 20, 'bold'),
                bg='white',
                fg=self.colors['primary']).pack(pady=(30, 20))
        
        # Registration fields
        fields = ["Username", "Password", "City", "Phone", "Address"]
        self.reg_entries = {}
        
        # Create two columns for fields
        field_frame = tk.Frame(register_frame, bg='white')
        field_frame.pack(fill=tk.X, pady=10, padx=40)
        
        left_frame = tk.Frame(field_frame, bg='white')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        right_frame = tk.Frame(field_frame, bg='white')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
        
        # Add fields to appropriate frames
        for i, field in enumerate(fields):
            if i < 3:  # First three fields in left column
                parent_frame = left_frame
            else:  # Remaining fields in right column
                parent_frame = right_frame
                
            #show = "*" if field == "Password" else None
            field_frame, entry = self.create_entry_field(parent_frame, field)
            field_frame.pack(pady=10, fill=tk.X)
            self.reg_entries[field] = entry
        
        # Buttons
        button_frame = tk.Frame(register_frame, bg='white')
        button_frame.pack(pady=30)
        
        submit_btn = self.create_fancy_button(button_frame, "Create Account", self.handle_register, self.colors['accent'])
        submit_btn.pack(side=tk.LEFT, padx=10)
        
        back_btn = self.create_fancy_button(button_frame, "Back to Login", self.show_login, self.colors['secondary'])
        back_btn.pack(side=tk.LEFT, padx=10)

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields", parent=self.root)
            return
            
        user_id = login_user(username, password)
        
        if user_id:
            self.current_user = user_id
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials", parent=self.root)

    def handle_register(self):
        # Validate required fields
        for field, entry in self.reg_entries.items():
            if not entry.get().strip():
                messagebox.showerror("Error", f"{field} field cannot be empty", parent=self.root)
                return
        
        user_id = str(uuid.uuid4())[:8]
        success = register_user(
            user_id,
            self.reg_entries["Username"].get(),
            self.reg_entries["Password"].get(),
            self.reg_entries["City"].get(),
            self.reg_entries["Phone"].get(),
            self.reg_entries["Address"].get()
        )
        
        if success:
            messagebox.showinfo("Success", "Registration successful! You can now login.", parent=self.root)
            self.show_login()
        else:
            messagebox.showerror("Error", "Registration failed. Please try again.", parent=self.root)

    # Main Dashboard
    def show_dashboard(self):
        self.clear_frame()
        self.create_header("Stock Prediction Dashboard", show_back=False)
        
        main_frame = tk.Frame(self.root, bg=self.colors['background'])
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Welcome message
        welcome_frame = tk.Frame(main_frame, bg=self.colors['background'])
        welcome_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(welcome_frame, 
                text="Welcome to Stock Prediction System",
                font=('Helvetica', 24, 'bold'),
                bg=self.colors['background'],
                fg=self.colors['primary']).pack(pady=10)
        
        tk.Label(welcome_frame, 
                text="Make intelligent investment decisions with AI-powered predictions",
                font=('Helvetica', 14),
                bg=self.colors['background'],
                fg=self.colors['dark']).pack(pady=5)
        
        # Menu options in a card-like layout
        options_frame = tk.Frame(main_frame, bg=self.colors['background'])
        options_frame.pack(expand=True, fill=tk.BOTH, pady=20)
        
        # Create three cards
        card_frame1 = tk.Frame(options_frame, 
                              bg='white',
                              bd=0,
                              relief=tk.SOLID,
                              highlightthickness=1,
                              highlightbackground=self.colors['light'])
        card_frame1.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=15, pady=10)
        
        card_frame2 = tk.Frame(options_frame, 
                              bg='white',
                              bd=0,
                              relief=tk.SOLID,
                              highlightthickness=1,
                              highlightbackground=self.colors['light'])
        card_frame2.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=15, pady=10)
        
        card_frame3 = tk.Frame(options_frame, 
                              bg='white',
                              bd=0,
                              relief=tk.SOLID,
                              highlightthickness=1,
                              highlightbackground=self.colors['light'])
        card_frame3.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=15, pady=10)
        
        # Card 1 content
        tk.Label(card_frame1, 
                text="Single Stock Prediction",
                font=('Helvetica', 16, 'bold'),
                bg='white',
                fg=self.colors['primary']).pack(pady=(20, 10))
        
        tk.Label(card_frame1, 
                text="Analyze and predict the future price of a specific stock",
                font=('Helvetica', 12),
                bg='white',
                wraplength=250,
                fg=self.colors['dark']).pack(pady=10, padx=15)
        
        self.create_fancy_button(card_frame1, "Predict Stock", self.show_single_prediction, 
                               self.colors['secondary'], width=15).pack(pady=20)
        
        # Card 2 content
        tk.Label(card_frame2, 
                text="Stock Recommendations",
                font=('Helvetica', 16, 'bold'),
                bg='white',
                fg=self.colors['primary']).pack(pady=(20, 10))
        
        tk.Label(card_frame2, 
                text="Get AI recommendations for the best stocks to invest in",
                font=('Helvetica', 12),
                bg='white',
                wraplength=250,
                fg=self.colors['dark']).pack(pady=10, padx=15)
        
        self.create_fancy_button(card_frame2, "Get Recommendations", self.show_recommendation_window, 
                               self.colors['accent'], width=18).pack(pady=20)
        
        # Card 3 content
        tk.Label(card_frame3, 
                text="Prediction History",
                font=('Helvetica', 16, 'bold'),
                bg='white',
                fg=self.colors['primary']).pack(pady=(20, 10))
        
        tk.Label(card_frame3, 
                text="View your past predictions and investment recommendations",
                font=('Helvetica', 12),
                bg='white',
                wraplength=250,
                fg=self.colors['dark']).pack(pady=10, padx=15)
        
        self.create_fancy_button(card_frame3, "View History", self.show_history, 
                               self.colors['primary'], width=15).pack(pady=20)
        
        # Footer with logout button
        footer_frame = tk.Frame(main_frame, bg=self.colors['background'], height=50)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        logout_btn = tk.Button(footer_frame, 
                              text="Logout",
                              font=('Helvetica', 12),
                              bg=self.colors['warning'],
                              fg='white',
                              bd=0,
                              padx=15,
                              pady=8,
                              cursor="hand2",
                              command=self.show_login)
        logout_btn.pack(side=tk.RIGHT, padx=20)

    def show_single_prediction(self):
        self.clear_frame()
        header = self.create_header("Single Stock Prediction")
        
        main_frame = tk.Frame(self.root, bg=self.colors['background'])
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Controls panel
        controls_frame = tk.Frame(main_frame, 
                                 bg='white',
                                 bd=0,
                                 relief=tk.SOLID,
                                 highlightthickness=1,
                                 highlightbackground=self.colors['light'])
        controls_frame.pack(fill=tk.X, pady=10)
        
        control_padding = 15
        
        # Stock selection
        stock_label = tk.Label(controls_frame, 
                              text="Select Stock:",
                              font=('Helvetica', 12, 'bold'),
                              bg='white',
                              fg=self.colors['dark'])
        stock_label.pack(side=tk.LEFT, padx=control_padding, pady=control_padding)
        
        self.stock_var = tk.StringVar()
        stock_dropdown = ttk.Combobox(controls_frame, 
                                     textvariable=self.stock_var, 
                                     values=STOCKS, 
                                     width=20,
                                     font=('Helvetica', 11))
        stock_dropdown.pack(side=tk.LEFT, padx=5, pady=control_padding)
        
        # Predict button
        predict_btn = tk.Button(controls_frame, 
                               text="Predict Stock Price",
                               font=('Helvetica', 12),
                               bg=self.colors['accent'],
                               fg='white',
                               padx=15,
                               pady=5,
                               bd=0,
                               cursor="hand2",
                               command=self.run_single_prediction)
        predict_btn.pack(side=tk.LEFT, padx=control_padding*2, pady=control_padding)
        
        # Graph panel
        graph_panel = tk.Frame(main_frame, 
                              bg='white',
                              bd=0,
                              relief=tk.SOLID,
                              highlightthickness=1,
                              highlightbackground=self.colors['light'])
        graph_panel.pack(expand=True, fill=tk.BOTH, pady=10)
        
        # Status panel
        status_frame = tk.Frame(graph_panel, bg='white')
        status_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        
        self.status_label = tk.Label(status_frame, 
                                   text="Select a stock and click 'Predict Stock Price' to view forecast",
                                   font=('Helvetica', 11, 'italic'),
                                   bg='white',
                                   fg=self.colors['dark'])
        self.status_label.pack(pady=5)
        
        # Graph container
        self.graph_frame = tk.Frame(graph_panel, bg='white')
        self.graph_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def run_single_prediction(self):
        try:
            stock = self.stock_var.get()
        except AttributeError:
            self.show_single_prediction()
            return
        
        if not stock:
            messagebox.showerror("Error", "Please select a stock", parent=self.root)
            return
        
        self.status_label.config(text=f"Generating prediction for {stock}...", fg=self.colors['dark'])
        self.root.update()
        
        prediction, actual = predict_single_stock(stock)
        if prediction is None:
            self.status_label.config(text=f"Failed to get prediction for {stock}", fg=self.colors['warning'])
            return
        
        # Ensure prediction and actual are lists of numbers
        try:
            prediction = [float(np.array(p).item()) for p in prediction]
            actual = [float(np.array(a).item()) for a in actual] if actual is not None and len(actual) > 0 else []
        except (ValueError, TypeError) as e:
            print(f"Error converting data to floats: {e}")
            self.status_label.config(text=f"Invalid data format for {stock}", fg=self.colors['warning'])
            return
        
        # Calculate profit if we have actual data
        profit = 0
        if actual:
            try:
                profit = float(prediction[-1]) - float(actual[-1])
            except (ValueError, TypeError) as e:
                print(f"Error calculating profit: {e}")
                profit = 0
        
        # Save to database
        try:
            save_single_prediction(
                user_id=self.current_user,
                stock_name=stock.replace('.NS', ''),
                time_period=10,
                predicted_profit=float(profit) if profit is not None else 0
            )
        except Exception as e:
            print(f"Error saving prediction: {e}")
        
        # Clear existing graph
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        
        # Create dates for x-axis
        today = datetime.now()
        if actual:
            past_dates = [(today - timedelta(days=len(actual)-i)).strftime('%d-%b') for i in range(len(actual))]
            future_dates = [(today + timedelta(days=i+1)).strftime('%d-%b') for i in range(len(prediction))]
            all_dates = past_dates + future_dates
            combined_data = actual + prediction[1:]
        else:
            past_dates = []
            future_dates = [(today + timedelta(days=i)).strftime('%d-%b') for i in range(len(prediction))]
            all_dates = future_dates
            combined_data = prediction
        
        # Create figure and plot data with improved styling
        plt.style.use('ggplot')
        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor('white')
        
        if actual:
            x_actual = np.arange(len(past_dates))
            ax.plot(x_actual, actual, marker='o', linewidth=2.5, 
                   color=self.colors['primary'], markersize=8, 
                   markerfacecolor='white', label='Current Price')
            
            # Plot predicted data starting from the last actual value
            x_combined = np.arange(len(all_dates))
            try:
                y_pred = [actual[-1]] + prediction[1:]
                x_pred_start = len(actual) - 1
                x_pred_end = x_pred_start + len(y_pred)
                ax.plot(x_combined[x_pred_start:x_pred_end], y_pred, marker='o', linewidth=2.5, 
                       color=self.colors['accent'], markersize=8, 
                       markerfacecolor='white', label='Predicted Price')
                
                # Add price labels for actual data
                for i, price in enumerate(actual):
                    ax.annotate(f'₹{price:.2f}', 
                               (x_actual[i], price),
                               textcoords="offset points", 
                               xytext=(0,10), 
                               ha='center',
                               fontsize=9,
                               color=self.colors['primary'])
                
                # Add price labels for predicted data
                for i, price in enumerate(y_pred):
                    ax.annotate(f'₹{price:.2f}', 
                               (x_combined[x_pred_start + i], price),
                               textcoords="offset points", 
                               xytext=(0,10), 
                               ha='center',
                               fontsize=9,
                               fontweight='bold',
                               color=self.colors['accent'])
                
                # Add today marker with improved styling
                ax.axvline(x=len(past_dates)-0.5, color=self.colors['dark'], linestyle='--', alpha=0.7, linewidth=1.5)
                
                # Add 'Today' label with better positioning and styling
                ax.annotate('Today', 
                           (len(past_dates)-0.5, ax.get_ylim()[0]),
                           xytext=(0, -25),
                           textcoords="offset points",
                           ha='center',
                           fontsize=10,
                           fontweight='bold',
                           color=self.colors['dark'],
                           bbox=dict(boxstyle="round,pad=0.3", fc='white', ec=self.colors['dark'], alpha=0.7))
                
                # Add a gradient background for the prediction area
                ax.axvspan(len(past_dates)-0.5, len(all_dates), alpha=0.1, color=self.colors['accent'])
                
            except Exception as e:
                print(f"Error plotting prediction: {e}")
                self.status_label.config(text=f"Failed to plot prediction for {stock}", fg=self.colors['warning'])
                return
        else:
            x_pred = np.arange(len(future_dates))
            ax.plot(x_pred, prediction, marker='o', linewidth=2.5, 
                   color=self.colors['accent'], markersize=8, 
                   markerfacecolor='white', label='Predicted Price')
            
            # Add price labels for predictions
            for i, price in enumerate(prediction):
                ax.annotate(f'₹{price:.2f}', 
                          (x_pred[i], price),
                          textcoords="offset points", 
                          xytext=(0,10), 
                          ha='center',
                          fontsize=9,
                          fontweight='bold',
                          color=self.colors['accent'])
            
            # Add a gradient background for the prediction area
            ax.axvspan(0, len(future_dates), alpha=0.1, color=self.colors['accent'])
        
        # Set labels and title with improved styling
        ax.set_xlabel('Date', fontsize=12, fontweight='bold', color=self.colors['dark'])
        ax.set_ylabel('Price (₹)', fontsize=12, fontweight='bold', color=self.colors['dark'])
        
        # Better title with stock name highlighted
        ax.set_title(f'Price Prediction for {stock}', 
                    fontsize=16, 
                    fontweight='bold', 
                    color=self.colors['primary'],
                    pad=15)
        
        # Improve x-axis and grid
        ax.set_xticks(range(len(all_dates)))
        ax.set_xticklabels(all_dates, rotation=45, ha='right')
        ax.grid(True, linestyle='--', alpha=0.7, color=self.colors['light'])
        
        # Legend with better styling
        legend = ax.legend(loc='upper left', 
                         frameon=True, 
                         fancybox=True, 
                         framealpha=0.9,
                         shadow=True,
                         fontsize=10)
        frame = legend.get_frame()
        frame.set_facecolor('white')
        frame.set_edgecolor(self.colors['light'])
        
        plt.tight_layout()
        
        # Add the plot to the frame
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Set status with profit info
        profit_str = f"Predicted Profit: {'₹' + format(profit, '.2f') if profit > 0 else '-₹' + format(abs(profit), '.2f')}"
        status_color = self.colors['profit'] if profit > 0 else self.colors['loss']
        self.status_label.config(
            text=f"Prediction complete for {stock}. {profit_str}",
            fg=status_color,
            font=('Helvetica', 12, 'bold')
        )

    # Stock Recommendation System
    def show_recommendation_window(self):
        self.rec_window = tk.Toplevel(self.root)
        self.rec_window.title("Stock Recommendations")
        self.rec_window.geometry("600x650")
        self.rec_window.configure(bg=self.colors['background'])
        self.rec_window.resizable(False, False)
        
        # Create header
        header_frame = tk.Frame(self.rec_window, bg=self.colors['primary'], height=70)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, 
                text="Smart Stock Recommendations",
                font=('Helvetica', 18, 'bold'),
                fg=self.colors['light'],
                bg=self.colors['primary']).pack(side=tk.LEFT, padx=20, pady=15)
        
        # Main content area
        content_frame = tk.Frame(self.rec_window, bg=self.colors['background'])
        content_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Investment parameters section
        params_frame = tk.Frame(content_frame, 
                              bg='white',
                              bd=0,
                              relief=tk.SOLID,
                              highlightthickness=1,
                              highlightbackground=self.colors['light'])
        params_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(params_frame, 
                text="Investment Parameters",
                font=('Helvetica', 16, 'bold'),
                bg='white',
                fg=self.colors['primary']).pack(pady=(15, 20))
        
        # Amount field with currency symbol
        amount_frame = tk.Frame(params_frame, bg='white')
        amount_frame.pack(fill=tk.X, padx=40, pady=10)
        
        tk.Label(amount_frame, 
                text="Amount to Invest:",
                font=('Helvetica', 12),
                bg='white',
                fg=self.colors['dark']).pack(side=tk.LEFT, padx=5)
        
        currency_label = tk.Label(amount_frame, 
                                 text="₹",
                                 font=('Helvetica', 14, 'bold'),
                                 bg='white',
                                 fg=self.colors['dark'])
        currency_label.pack(side=tk.LEFT, padx=(20, 0))
        
        self.amount_entry = tk.Entry(amount_frame, 
                                    font=('Helvetica', 12),
                                    bd=0,
                                    relief=tk.SOLID,
                                    highlightthickness=1,
                                    highlightbackground=self.colors['secondary'],
                                    highlightcolor=self.colors['accent'],
                                    width=15)
        self.amount_entry.pack(side=tk.LEFT, padx=(0, 5), ipady=5)
        
        # Period field
        period_frame = tk.Frame(params_frame, bg='white')
        period_frame.pack(fill=tk.X, padx=40, pady=10)
        
        tk.Label(period_frame, 
                text="Investment Period:",
                font=('Helvetica', 12),
                bg='white',
                fg=self.colors['dark']).pack(side=tk.LEFT, padx=5)
        
        self.period_entry = tk.Entry(period_frame, 
                                   font=('Helvetica', 12),
                                   bd=0,
                                   relief=tk.SOLID,
                                   highlightthickness=1,
                                   highlightbackground=self.colors['secondary'],
                                   highlightcolor=self.colors['accent'],
                                   width=10)
        self.period_entry.pack(side=tk.LEFT, padx=(20, 5), ipady=5)
        
        tk.Label(period_frame, 
                text="days",
                font=('Helvetica', 12),
                bg='white',
                fg=self.colors['dark']).pack(side=tk.LEFT)
        
        # Generate button
        button_frame = tk.Frame(params_frame, bg='white')
        button_frame.pack(pady=20)
        
        generate_btn = tk.Button(button_frame, 
                                text="Generate Recommendations",
                                font=('Helvetica', 13, 'bold'),
                                bg=self.colors['accent'],
                                fg='white',
                                padx=20,
                                pady=10,
                                bd=0,
                                cursor="hand2",
                                command=self.generate_recommendations)
        generate_btn.pack()
        
        # Results section
        results_frame = tk.Frame(content_frame, 
                               bg='white',
                               bd=0,
                               relief=tk.SOLID,
                               highlightthickness=1,
                               highlightbackground=self.colors['light'])
        results_frame.pack(expand=True, fill=tk.BOTH, pady=10)
        
        tk.Label(results_frame, 
                text="Recommendations Results",
                font=('Helvetica', 16, 'bold'),
                bg='white',
                fg=self.colors['primary']).pack(pady=(15, 10))
        
        # Results text widget with scrollbar
        text_frame = tk.Frame(results_frame, bg='white')
        text_frame.pack(expand=True, fill=tk.BOTH, padx=15, pady=10)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.rec_results = tk.Text(text_frame, 
                                  wrap=tk.WORD, 
                                  height=15, 
                                  width=60,
                                  font=('Helvetica', 11),
                                  bd=0,
                                  padx=10,
                                  pady=10,
                                  relief=tk.SOLID,
                                  highlightthickness=1,
                                  highlightbackground=self.colors['light'],
                                  yscrollcommand=scrollbar.set)
        self.rec_results.pack(expand=True, fill=tk.BOTH)
        scrollbar.config(command=self.rec_results.yview)
        
        # Initialize with placeholder text
        self.rec_results.insert(tk.END, "Your investment recommendations will appear here...")
        self.rec_results.config(state=tk.DISABLED)

    def generate_recommendations(self):
        # Re-enable text widget for modification
        self.rec_results.config(state=tk.NORMAL)
        self.rec_results.delete(1.0, tk.END)
        self.rec_results.insert(tk.END, "Generating recommendations, please wait...")
        self.rec_results.update()
        
        try:
            amount = float(self.amount_entry.get())
            days = int(self.period_entry.get())
            if amount <= 0 or days <= 0:
                raise ValueError("Positive values required")
        except ValueError as e:
            self.rec_results.delete(1.0, tk.END)
            self.rec_results.insert(tk.END, "⚠️ Error: Please enter valid positive numbers for amount and days.")
            self.rec_results.config(state=tk.DISABLED)
            return
        
        recommendations = predict_all_stocks(amount, days)
        if not recommendations:
            self.rec_results.delete(1.0, tk.END)
            self.rec_results.insert(tk.END, "⚠️ No recommendations could be generated. Please try again later.")
            self.rec_results.config(state=tk.DISABLED)
            return
        
        best = recommendations[0]
        try:
            save_recommendation_prediction(
                user_id=self.current_user,
                stock_name=best['stock'],
                investment_amount=float(amount),
                time_period=int(days),
                predicted_profit=float(best['profit'])
            )
        except Exception as e:
            print(f"Error saving recommendation: {e}")
        
        # Clear and add header
        self.rec_results.delete(1.0, tk.END)
        
        # Insert fancy formatted header
        self.rec_results.insert(tk.END, "📊 Top Stock Recommendations\n", "header")
        self.rec_results.insert(tk.END, "═══════════════════════════════\n\n", "divider")
        
        self.rec_results.insert(tk.END, f"Investment Amount: ", "label")
        self.rec_results.insert(tk.END, f"₹{amount:,.2f}\n", "value")
        
        self.rec_results.insert(tk.END, f"Investment Period: ", "label")
        self.rec_results.insert(tk.END, f"{days} days\n\n", "value")
        
        # Add recommendations with improved formatting
        for i, stock in enumerate(recommendations[:3], 1):
            profit_percent = stock['profit']/amount*100
            profit_color = "profit" if stock['profit'] > 0 else "loss"
            
            # Add stock header with rank
            self.rec_results.insert(tk.END, f"#{i} ", "rank")
            self.rec_results.insert(tk.END, f"{stock['stock']}\n", "stock_name")
            
            # Add stock details
            self.rec_results.insert(tk.END, f"   • Current Price: ", "label")
            self.rec_results.insert(tk.END, f"₹{stock['current_price']:,.2f}\n", "value")
            
            self.rec_results.insert(tk.END, f"   • Predicted Price: ", "label")
            self.rec_results.insert(tk.END, f"₹{stock['predicted_price']:,.2f}\n", "value")
            
            self.rec_results.insert(tk.END, f"   • Expected Profit: ", "label")
            
            if stock['profit'] > 0:
                self.rec_results.insert(tk.END, f"₹{stock['profit']:,.2f} (+{profit_percent:.1f}%)\n\n", profit_color)
            else:
                self.rec_results.insert(tk.END, f"-₹{abs(stock['profit']):,.2f} ({profit_percent:.1f}%)\n\n", profit_color)
        
        # Text tags for styling
        self.rec_results.tag_configure("header", font=('Helvetica', 14, 'bold'), foreground=self.colors['primary'])
        self.rec_results.tag_configure("divider", foreground=self.colors['primary'])
        self.rec_results.tag_configure("label", font=('Helvetica', 11), foreground=self.colors['dark'])
        self.rec_results.tag_configure("value", font=('Helvetica', 11, 'bold'))
        self.rec_results.tag_configure("rank", font=('Helvetica', 12, 'bold'), foreground=self.colors['secondary'])
        self.rec_results.tag_configure("stock_name", font=('Helvetica', 13, 'bold'), foreground=self.colors['primary'])
        self.rec_results.tag_configure("profit", foreground=self.colors['profit'], font=('Helvetica', 11, 'bold'))
        self.rec_results.tag_configure("loss", foreground=self.colors['loss'], font=('Helvetica', 11, 'bold'))
        
        # Disable editing
        self.rec_results.config(state=tk.DISABLED)

    # Prediction History
    def show_history(self):
        self.clear_frame()
        self.create_header("Prediction History")
        
        main_frame = tk.Frame(self.root, bg=self.colors['background'])
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Frame for filters and controls (future enhancement potential)
        controls_frame = tk.Frame(main_frame, bg=self.colors['background'])
        controls_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(controls_frame, 
                text="Your Prediction History",
                font=('Helvetica', 16, 'bold'),
                bg=self.colors['background'],
                fg=self.colors['primary']).pack(side=tk.LEFT)
        
        # Get user predictions
        history = get_user_predictions(self.current_user)
        
        # Create table container
        table_frame = tk.Frame(main_frame, 
                              bg='white',
                              bd=0,
                              relief=tk.SOLID,
                              highlightthickness=1,
                              highlightbackground=self.colors['light'])
        table_frame.pack(expand=True, fill=tk.BOTH, pady=10)
        
        if not history:
            # Show empty state
            empty_frame = tk.Frame(table_frame, bg='white')
            empty_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=30)
            
            tk.Label(empty_frame, 
                    text="No prediction history found",
                    font=('Helvetica', 14),
                    bg='white',
                    fg=self.colors['dark']).pack(pady=10)
            
            tk.Label(empty_frame, 
                    text="Make some predictions to see your history here",
                    font=('Helvetica', 12),
                    bg='white',
                    fg=self.colors['dark']).pack(pady=5)
            
            return
        
        # Create table with scrollbar
        tree_frame = tk.Frame(table_frame)
        tree_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        tree_scroll_y = tk.Scrollbar(tree_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree_scroll_x = tk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        columns = ("Stock", "Type", "Amount", "Period", "Profit", "Time")
        tree = ttk.Treeview(tree_frame, 
                          columns=columns, 
                          show="headings", 
                          yscrollcommand=tree_scroll_y.set,
                          xscrollcommand=tree_scroll_x.set)
        
        # Configure column headings with better styling
        for col in columns:
            tree.heading(col, text=col)
            # Center alignment for all columns
            tree.column(col, anchor=tk.CENTER)
        
        # Set column widths
        tree.column("Stock", width=100)
        tree.column("Type", width=120)
        tree.column("Amount", width=120)
        tree.column("Period", width=100)
        tree.column("Profit", width=120)
        tree.column("Time", width=150)
        
        # Alternating row colors
        tree.tag_configure('oddrow', background=self.colors['light'])
        tree.tag_configure('evenrow', background='white')
        
        # Profit/Loss color coding
        tree.tag_configure('profit', foreground=self.colors['profit'])
        tree.tag_configure('loss', foreground=self.colors['loss'])
        
        # Populate tree with data
        for i, pred in enumerate(history):
            # Format display values
            amount = f"₹{pred['amount']:,.2f}" if pred['amount'] and pred['amount'] > 0 else "N/A"
            
            # Set row tags for styling
            tags = ('oddrow',) if i % 2 else ('evenrow',)
            
            # Add profit/loss tag if applicable
            if pred['predicted_profit'] is not None:
                if pred['predicted_profit'] > 0:
                    profit_str = f"₹{pred['predicted_profit']:,.2f}"
                    tags = tags + ('profit',)
                else:
                    profit_str = f"-₹{abs(pred['predicted_profit']):,.2f}"
                    tags = tags + ('loss',)
            else:
                profit_str = "N/A"
            
            # Insert row with formatting
            tree.insert("", "end", 
                      values=(
                          pred['stock_name'],
                          pred['prediction_type'].capitalize(),
                          amount,
                          f"{pred['time_period']} days" if pred['time_period'] else "N/A",
                          profit_str,
                          pred['prediction_time'].strftime("%Y-%m-%d %H:%M")
                      ),
                      tags=tags)
        
        # Pack tree with scrollbars
        tree.pack(expand=True, fill=tk.BOTH)
        tree_scroll_y.config(command=tree.yview)
        tree_scroll_x.config(command=tree.xview)
        
        # History stats summary at bottom
        stats_frame = tk.Frame(main_frame, bg=self.colors['background'])
        stats_frame.pack(fill=tk.X, pady=10)
        
        # Calculate some basic stats
        total_predictions = len(history)
        profitable_predictions = sum(1 for p in history if p['predicted_profit'] and p['predicted_profit'] > 0)
        
        if total_predictions > 0:
            success_rate = (profitable_predictions / total_predictions) * 100
        else:
            success_rate = 0
        
        stats_text = f"Total Predictions: {total_predictions} | Profitable: {profitable_predictions} | Success Rate: {success_rate:.1f}%"
        
        tk.Label(stats_frame, 
                text=stats_text,
                font=('Helvetica', 12),
                bg=self.colors['background'],
                fg=self.colors['dark']).pack(side=tk.LEFT, padx=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = StockApp(root)
    root.mainloop()
