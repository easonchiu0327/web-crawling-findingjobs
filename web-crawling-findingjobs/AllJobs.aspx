<%@ Page Title="About" Language="C#" MasterPageFile="~/Site.Master" AutoEventWireup="true" CodeBehind="AllJobs.aspx.cs" Inherits="web_crawling_findingjobs.About" %>

<asp:Content ID="BodyContent" ContentPlaceHolderID="MainContent" runat="server">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">

    <style>

    </style>

    <!-- Data Sources -->
    <asp:ObjectDataSource runat="server"
        ID="odsJobs"
        SelectMethod="SellectALL"
        TypeName="web_crawling_findingjobs.JobListLogic.JobUtils.JobUtilities">
    </asp:ObjectDataSource>
    <!-- UI Components -->
    <div class="container my-4">
        <div class="mb-2">
            <h1 class="fw-bold">IT Job Listing in Saskatchewan</h1>
        </div>
    </div>
    <!-- Subtitle Section -->
    <div class="mb-4">
        <h2 class="h5 text-muted">This is the entire job collection — some explanation</h2>
    </div>
    <!-- Responsive table wrapper -->
    <div class="table-responsive">
        <asp:GridView 
            ID="grdJobs" 
            runat="server" 
            AutoGenerateColumns="False" 
            DataSourceID="odsJobs"
            CssClass="table table-bordered table-sm align-middle jobs-grid">
            <Columns>
                <asp:BoundField DataField="Id" HeaderText="Id" SortExpression="Id"></asp:BoundField>
                <asp:BoundField DataField="CompanyName" HeaderText="CompanyName" SortExpression="CompanyName"></asp:BoundField>
                <asp:BoundField DataField="JobTitle" HeaderText="JobTitle" SortExpression="JobTitle"></asp:BoundField>
                <asp:BoundField DataField="Location" HeaderText="Location" SortExpression="Location"></asp:BoundField>
                <asp:BoundField DataField="Category" HeaderText="Category" SortExpression="Category"></asp:BoundField>
                <asp:BoundField DataField="Skills" HeaderText="Skills" SortExpression="Skills"></asp:BoundField>
                <asp:BoundField DataField="Years" HeaderText="Years" SortExpression="Years"></asp:BoundField>
                <asp:BoundField DataField="CitizePR" HeaderText="CitizePR" SortExpression="CitizePR"></asp:BoundField>
                <asp:TemplateField HeaderText="Link">
                    <ItemTemplate>
                        <asp:HyperLink runat="server" Target="_blank"
                            NavigateUrl='<%# Eval("Link") %>'
                            Text="View"
                            CssClass="btn btn-sm btn-primary" />
                    </ItemTemplate>
                </asp:TemplateField>
            </Columns>
        </asp:GridView>
    </div>

    <div class="mb-4">
        <h2 class="h5 text-muted">Just some random pop up</h2>
    </div>
    <div class="table-responsive">

        <asp:Timer ID="timerRandomJob" runat="server" Interval="10000" OnTick="timerRandomJob_Tick"></asp:Timer>
        <!-- the timer is going to drive the updatepanel, so there is a trigger in the update panel that control by the timer ID -->
        <asp:UpdatePanel ID="updatePanelRandomJob" runat="server">
            <Triggers>
                <asp:AsyncPostBackTrigger ControlID="timerRandomJob" />
            </Triggers>
            <ContentTemplate>
                <!-- Data source for the random grid -->
                <asp:ObjectDataSource ID="odjJobsRandom" runat="server"
                    SelectMethod="SellectRandomJob"
                    TypeName="web_crawling_findingjobs.JobListLogic.JobUtils.JobUtilities"></asp:ObjectDataSource>
                <asp:GridView ID="grdRandomJob"
                    runat="server"
                    AutoGenerateColumns="False"
                    DataSourceID="odjJobsRandom"
                    CssClass="table table-bordered table-sm align-middle jobs-grid"
                    EmptyDataText="No jobs found.">
                    <%--subtle header styling via Bootstrap--%>
                    <HeaderStyle CssClass="table-light" />
                    <Columns>
                        <asp:BoundField DataField="Id" HeaderText="Id" SortExpression="Id">
                            <ItemStyle CssClass="truncate" Width="80px"/>
                        </asp:BoundField>
                        <asp:BoundField DataField="CompanyName" HeaderText="CompanyName" SortExpression="CompanyName">
                            <ItemStyle CssClass="truncate" Width="180px"/>
                        </asp:BoundField>
                        <asp:BoundField DataField="JobTitle" HeaderText="JobTitle" SortExpression="JobTitle">
                            <ItemStyle CssClass="truncate" Width="240px"/>
                        </asp:BoundField>
                        <asp:BoundField DataField="Location" HeaderText="Location" SortExpression="Location">
                            <ItemStyle CssClass="truncate" Width="140px"/>
                        </asp:BoundField>
                        <asp:BoundField DataField="Category" HeaderText="Category" SortExpression="Category">
                            <ItemStyle CssClass="truncate" Width="140px"/>
                        </asp:BoundField>
                        <%--Long text should wrap--%>
                        <asp:BoundField DataField="Skills" HeaderText="Skills" SortExpression="Skills">
                            <ItemStyle CssClass="wrap" Width="420px"/>
                        </asp:BoundField>
                        <asp:BoundField DataField="Years" HeaderText="Years" SortExpression="Years">
                            <ItemStyle CssClass="truncate" Width="100px"/>
                        </asp:BoundField>
                        <asp:BoundField DataField="CitizePR" HeaderText="CitizePR" SortExpression="CitizePR">
                            <ItemStyle CssClass="truncate" Width="120px"/>
                        </asp:BoundField>
                        <%--Short Bootstrap-styled "View" link--%>
                        <asp:TemplateField HeaderText="Link">
                            <ItemStyle Width="100px" />
                            <ItemTemplate>
                                <asp:HyperLink runat="server"
                                    NavigateUrl='<%# Eval("Link") %>'
                                    Target="_blank"
                                    Text="View"
                                    CssClass="btn btn-sm btn-primary" />
                            </ItemTemplate>
                        </asp:TemplateField>
                    </Columns>
                </asp:GridView>
            </ContentTemplate>
        </asp:UpdatePanel>
    </div>
</asp:Content>
