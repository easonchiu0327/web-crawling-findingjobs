# Saskatchewan IT Job Listings Web App

This project is a **.NET WebForms application** that displays IT job postings in Saskatchewan.  
The backend data comes from a **Scrapy + Selenium web scraping bot** that stores job listings in **SQL Server (SSMS)**.  
The web app provides an **interactive GridView with filters and AJAX updates** using ASP.NET controls and Bootstrap styling.

# Skills
C#, ASP.NET, OOP, SQL Server, AJAX (UpdatePanel), GridView, DropDownList, Bootstrap 5

## Web UI Demo
- Page load
<img width="1361" height="850" alt="image" src="https://github.com/user-attachments/assets/24dddc3a-5285-4768-855c-c90d8f53620a" />

- Filter by Category
<img width="1351" height="837" alt="image" src="https://github.com/user-attachments/assets/94f4926a-6ec5-4b11-943b-90246df65793" />

- Filter by 3 dropdown list
<img width="1352" height="371" alt="image" src="https://github.com/user-attachments/assets/c3e1d555-7b77-49a2-86f9-96e66b02f0ea" />

# Features
- Dynamic filters: narrow results by Category + Company + PR together  
- GridView with AJAX partial postback for better UX  
- A Random Timer (updates every 10 seconds)  
- ObjectDataSource binding for dropdowns (Categories, Companies, PR)  

# Strategy Overview

## OOP + DAO Pattern
1. **Domain Model**
   - `Job` class represents a job listing with properties (`Id`, `Company`, `JobTitle`, etc.).
   - `Category` class represents a job listing with properties (`Id`, `Category`).
   - `Comapny` class represents a job listing with properties (`Id`, `Company`).
   - `CitizenPR` class represents a job listing with properties (`Id`, `Status`).

2. **DAO Layer (Data Access Objects)**
   - `JobUtilities` → Handles all SQL queries for job listings.
   - `CategoryUtilities` → Fetches categories.
   - `CompanyUtilities` → Fetches companies.
   - `CitizenPRUtilities` → Fetches PR requirements.

3. **Separation of Concerns**
   - **UI Layer**: ASPX + GridView + DropDownLists.
   - **Business Logic Layer**: Code-behind orchestrates filters and calls DAOs.
   - **Data Access Layer**: Utility/DAO classes encapsulate SQL Server queries.

---

## Stage 1: Data Source
- Data comes from **SQL Server** populated by the scraper.  
- Tables are normalized:  
  - `JobListings` (core)  
  - `Company` (lookup)  
  - `Category` (lookup)  
  - `CitizenPR` (lookup)

---

## Stage 2: UI Components
- **GridView** bound from code-behind (`List<Job>`).  
- Three **DropDownList** filters populated via `ObjectDataSource`:  
  - `odsCategory` → Categories  
  - `odsCompany` → Companies  
  - `odsCitizenPR` → PR status  
- Each dropdown has `OnSelectedIndexChanged` → triggers rebind of the grid.

---

## Stage 3: AJAX Partial Updates
- GridView sits inside an **UpdatePanel**.  
- The dropdowns are registered as **AsyncPostBackTrigger**.  
- Only the GridView area refreshes → smooth user experience.

---

## Stage 4: Random Job Spotlight
- A second UpdatePanel + Timer fetches a random job every 10 seconds.  
- Uses `JobUtilities.SelectRandom()` to refresh only the spotlight area.  

---

## Execution Flow

1. **Page loads (first time)**  
   - `odsCategory` calls `CategoryUtilities.SelectAll()` to fetch all categories.  
   - `ddlFilterCategory` binds (text = Category, value = Category_id).  

2. **User changes a dropdown filter**  
   - `AutoPostBack="True"` triggers a partial postback.  
   - `AsyncPostBackTrigger` ensures only the GridView area is refreshed.  
   - ASP.NET calls `ddlFilterCategory_SelectedIndexChanged()`, `ddlFilterCompany_SelectedIndexChanged()`, `ddlFilterCitizenPR_SelectedIndexChanged()`.  
   - Code-behind calls DAO(bind three filter at once):  
     ```csharp
     JobUtilities.JobSelectByFilter(categoryId, companyId, citizenPRId);
     ```

3. **Data returned from SQL**  
   - DAO runs SQL with dynamic filters:  
     ```sql
     WHERE (@CategoryId = 0 OR JobListings.Category_id = @CategoryId)
       AND (@CompanyId = 0 OR JobListings.Company_id = @CompanyId)
       AND (@CitizenPRId = 0 OR JobListings.CitizenPR_id = @CitizenPRId)
     ```  
   - Each record is mapped into a `Job` object.  
   - DAO returns a `List<Job>` to code-behind.

4. **UI updates**  
   - `GridView.DataSource = jobList;`  
   - `GridView.DataBind();`  
   - Only GridView HTML is re-rendered (thanks to UpdatePanel).

5. **Random Job Spotlight**  
   - Timer in a separate UpdatePanel triggers every 10 seconds.  
   - Calls `JobUtilities.SelectRandom()` and updates only the spotlight area.

# Key Points

1. **OOP + DAO Encapsulation**  
   - The project uses Object-Oriented Programming (OOP) with domain models (`Job`, `Category`, `Company`, `CitizenPR`).  
   - Data Access Objects (DAOs) like `JobUtilities`, `CategoryUtilities`, etc. encapsulate SQL queries and return strongly typed objects.  
   - UI never touches raw SQL directly → easier to maintain, test, and extend.

2. **Separation of Concerns**  
   - UI (ASPX + GridView + DropDownLists) handles only presentation.  
   - Code-behind is responsible for event handling and orchestration.  
   - DAO layer isolates database logic, ensuring modular and reusable code.

3. **Dynamic SQL Filtering**  
   - Queries are written with optional parameters.  
   - Example:  
     ```sql
     WHERE (@CategoryId = 0 OR JobListings.Category_id = @CategoryId)
     ```  
   - This avoids duplicated SQL statements and supports multi-filter combinations (Category + Company + PR).

4. **Partial Page Rendering with AJAX**  
   - `UpdatePanel` ensures that only the GridView or Spotlight section updates.  
   - Provides a smoother user experience without full-page reloads.  
   - Maintains state of filters and grid position during refresh.

5. **Random Spotlight Design**  
   - Timer + separate UpdatePanel allows job spotlight to update asynchronously.  
   - Does not interfere with GridView filter operations.  
   - Calls `JobUtilities.SelectRandom()` for variety in the UI.

6. **Scalability**  
   - New filters (e.g., Location, Job Type) can be added by:  
     - Extending the domain model.  
     - Adding new methods in DAO classes.  
     - Registering the new dropdown in UI.  
   - No need to rewrite the core architecture.

7. **Maintainability**  
   - DAO pattern reduces duplication of SQL logic.  
   - Strongly typed `List<Job>` ensures compile-time safety.  
   - Clean mapping of DB → Object → UI makes debugging easier.


### ⚠️ **Disclaimer**
- This project is for educational use only. 
- Always review and respect the robots.txt and terms of service of any website you scrape.
- AI output can be wrong, please verify on the original posting.
