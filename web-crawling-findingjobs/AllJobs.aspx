<%@ Page Title="About" Language="C#" Async="true" MasterPageFile="~/Site.Master" AutoEventWireup="true" CodeBehind="AllJobs.aspx.cs" Inherits="web_crawling_findingjobs.About" %>

<asp:Content ID="BodyContent" ContentPlaceHolderID="MainContent" runat="server">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <%--How does the code work here:
        1. Page loads (first time)
            1.1 odsCategory runs CategoryUtilities.SelectAll() to fetch all categories from DB.
            1.2 ddlFilterCategory binds to that data (Categories for text, Category_id for value).
        2. User changes the category in ddlFilterCategory
            2.1 AutoPostBack="True", the page triggers a partial postback
            2.2 The AsyncPostBackTrigger for ddlFilterCategory ensures only the GridView area refreshes (not the whole page).
            2.3 When user pick a category, ASP.NET calls ddlFilterCategory_SelectedIndexChanged(), internally calls your SQL method JobSelectByCategory() at code behind.
        3. Data returned to C# at code behind
            3.1 List<Job> is created from the SQL reader results.
            3.2 Each row is mapped into a Job object with fields like Company, JobTitle, Location, Category, etc.
            3.3 Bind results to GridView
        4. UI updates without full refresh
            4.1 Because of UpdatePanel, only the GridView HTML is re-rendered and sent back to the browser.
    --%>
    <!-- Data Sources -->
    <asp:ObjectDataSource runat="server"
        ID="odsJobs"
        SelectMethod="SelectByCategory"
        TypeName="web_crawling_findingjobs.JobListLogic.JobUtils.JobUtilities">
        <%--This select is controled by the dropdown filter--%>
        <%--<SelectParameters>
            <asp:Parameter Name="categoryId" Type="Int32"></asp:Parameter>
        </SelectParameters>--%>
    </asp:ObjectDataSource>
    <asp:ObjectDataSource runat="server" ID="odsCategory"
        SelectMethod="SelectAll"
        TypeName="web_crawling_findingjobs.JobListLogic.CategoryUtils.CategoryUtilities"></asp:ObjectDataSource>
    <asp:ObjectDataSource runat="server" ID="odsCompany"
        SelectMethod="SelectAll"
        TypeName="web_crawling_findingjobs.JobListLogic.CompanyUtils.CompanyUtilities"></asp:ObjectDataSource>
    <asp:ObjectDataSource runat="server" ID="odsCitizenPR"
        SelectMethod="SelectAll"
        TypeName="web_crawling_findingjobs.JobListLogic.CitizenPR.CitizenPRUtilities"></asp:ObjectDataSource>
    <!-- UI Components -->
    <div class="container my-4">
        <div class="mb-2">
            <h1 class="fw-bold">IT Job Listing in Saskatchewan</h1>
            <h2 class="h5 text-muted">Browse jobs and filter by category, company, or CitizenPR requirement.</h2>
        </div>
    </div>

    <!-- Filter Section -->
    <div class="container mb-4">
        <div class="row g-3">

            <div class="col-md-4">
                <label for="ddlFilterCategory">Filter by Category</label>
                <asp:DropDownList runat="server" ID="ddlFilterCategory"
                    DataSourceID="odsCategory"
                    DataTextField="Categories"
                    DataValueField="Category_id"
                    AutoPostBack="True"
                    AppendDataBoundItems="true"
                    OnSelectedIndexChanged="ddlFilterCategory_SelectedIndexChanged"
                    CssClass="form-select">
                    <%--allow viewing all movies--%>
                    <asp:ListItem Text="All Categories" Value="0" />
                </asp:DropDownList>
            </div>

            <div class="col-md-4">
                <label for="ddlFilterCompany">Filter by Company</label>
                <asp:DropDownList runat="server" ID="ddlFilterCompany"
                    DataSourceID="odsCompany"
                    DataTextField="Name"
                    DataValueField="Company_id"
                    AutoPostBack="True"
                    AppendDataBoundItems="true"
                    OnSelectedIndexChanged="ddlFilterCompany_SelectedIndexChanged"
                    CssClass="form-select">
                    <%--allow viewing all movies--%>
                    <asp:ListItem Text="All Company" Value="0" />
                </asp:DropDownList>
            </div>

            <div class="col-md-4">
                <label for="ddlFilterCitizenPR">Filter by CitizenPR</label>
                <asp:DropDownList runat="server" ID="ddlFilterCitizenPR"
                    DataSourceID="odsCitizenPR"
                    DataTextField="CitizenPR_status"
                    DataValueField="CitizenPR_id"
                    AutoPostBack="True"
                    AppendDataBoundItems="true"
                    OnSelectedIndexChanged="ddlFilterCitizenPR_SelectedIndexChanged"
                    CssClass="form-select">
                    <%--allow viewing all movies--%>
                    <asp:ListItem Text="All CitizenPR" Value="0" />
                </asp:DropDownList>
            </div>
        </div>
    </div>



    <!-- Wrap GridView in UpdatePanel for AJAX -->
    <!-- Set of technologies used to update web pages after page load.-->
    <!-- Allows developers to make updates without reloading the web page which allows for more dynamic content and a richer user experience.-->
    <!-- The page should not reload between selections-->
    <div class="container mb-5">
        <asp:UpdatePanel ID="UpdatePanelForGrdMovies" runat="server">
            <%--this trigger in the update panel is controlled by the Category, company and citizenPR filter--%>
            <Triggers>
                <asp:AsyncPostBackTrigger ControlID="ddlFilterCategory" />
                <asp:AsyncPostBackTrigger ControlID="ddlFilterCompany" />
                <asp:AsyncPostBackTrigger ControlID="ddlFilterCitizenPR" />
            </Triggers>
            <ContentTemplate>
                <div class="table-responsive">
                    <%--Name of the columns in gridvew (DataField="Company", "Category", etc.) depend on the alias names return from SQL.--%>
                    <%--The data source here on gridview is pointed at code behind--%>
                    <asp:GridView runat="server"
                        ID="grdJobs"
                        CssClass="table table-bordered table-sm align-middle jobs-grid"
                        AutoGenerateColumns="False">
                        <Columns>
                            <asp:BoundField DataField="Id" HeaderText="ID" />
                            <asp:BoundField DataField="Company" HeaderText="Company" />
                            <asp:BoundField DataField="JobTitle" HeaderText="Job Title" />
                            <asp:BoundField DataField="Location" HeaderText="Location" />
                            <asp:BoundField DataField="Category" HeaderText="Category" />
                            <asp:BoundField DataField="Skills" HeaderText="Skills" />
                            <asp:BoundField DataField="Years" HeaderText="Years" />
                            <asp:BoundField DataField="CitizenPR" HeaderText="CitizenPR" />
                            <%--URL as Bootstrap butto--%>
                            <asp:TemplateField HeaderText="Link">
                                <ItemTemplate>
                                    <a href='<%# Eval("Link") %>' target="_blank"
                                        class="btn btn-sm btn-success">View Job
                                    </a>
                                </ItemTemplate>
                            </asp:TemplateField>
                        </Columns>
                    </asp:GridView>
                </div>
            </ContentTemplate>
        </asp:UpdatePanel>
    </div>


    <!-- Random Job Section -->
    <div class="container mb-5">
        <h3 class="h5 text-muted">Is this the job you are looking for?</h3>
        <asp:Timer ID="timerRandomJob" runat="server" Interval="10000" OnTick="timerRandomJob_Tick"></asp:Timer>
        <!-- the timer is going to drive the updatepanel, so there is a trigger in the update panel that control by the timer ID -->
        <asp:UpdatePanel ID="updatePanelRandomJob" runat="server">
            <Triggers>
                <asp:AsyncPostBackTrigger ControlID="timerRandomJob" />
            </Triggers>
            <ContentTemplate>
                <!-- Data source for the random grid -->
                <asp:ObjectDataSource ID="odjJobsRandom" runat="server"
                    SelectMethod="SelectRandomJob"
                    TypeName="web_crawling_findingjobs.JobListLogic.JobUtils.JobUtilities"></asp:ObjectDataSource>

                <asp:GridView ID="grdRandomJob"
                    runat="server"
                    AutoGenerateColumns="False"
                    CssClass="table table-bordered table-sm align-middle jobs-grid"
                    EmptyDataText="No jobs found." DataSourceID="odjJobsRandom">
                    <Columns>
                        <asp:BoundField DataField="Id" HeaderText="Id" SortExpression="Id"></asp:BoundField>
                        <asp:BoundField DataField="Company" HeaderText="Company" SortExpression="Company"></asp:BoundField>
                        <asp:BoundField DataField="JobTitle" HeaderText="JobTitle" SortExpression="JobTitle"></asp:BoundField>
                        <asp:BoundField DataField="Location" HeaderText="Location" SortExpression="Location"></asp:BoundField>
                        <asp:BoundField DataField="Category" HeaderText="Category" SortExpression="Category"></asp:BoundField>
                        <asp:BoundField DataField="Skills" HeaderText="Skills" SortExpression="Skills"></asp:BoundField>
                        <asp:BoundField DataField="Years" HeaderText="Years" SortExpression="Years"></asp:BoundField>
                        <asp:BoundField DataField="CitizenPR" HeaderText="CitizenPR" SortExpression="CitizenPR"></asp:BoundField>
                        <asp:TemplateField HeaderText="Link">
                            <ItemTemplate>
                                <a href='<%# Eval("Link") %>' target="_blank"
                                   class="btn btn-sm btn-success">View Job
                                </a>
                            </ItemTemplate>
                        </asp:TemplateField>
                    </Columns>
                </asp:GridView>
            </ContentTemplate>
        </asp:UpdatePanel>
    </div>
</asp:Content>
