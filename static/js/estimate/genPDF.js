function genPDF3(){
  {% for distri in distributor_list %}
  var doc = new jsPDF('p', 'mm', [215.9, 279.4]);

  doc.setFontSize(14);
  doc.setFontType("bold");
  doc.text(15, 20, 'PROJECT NAME: {{estimate.projectName}}');

  doc.addImage(imgData, 'JPEG', 150, 10, 50, 20)

  doc.setFontSize(12);
  doc.text(150, 41, 'Quotation #: {{estimate.estimateNumber}}');

  doc.text(15, 48, '      {{distri.distributorName}}')

  doc.setFontType("normal");
  doc.text(15, 41, 'To: {{distri.contactPerson}}')

  doc.setFontSize(11);
  doc.text(15, 55, '       {{distri.addressLine1}}')
  doc.text(15, 61, '       {{distri.addressLine2}}')
  doc.text(15, 67, '       {{distri.city}} {{distri.postalCode}}')
  doc.text(15, 73, '       {{distri.country}}');
  doc.text(15, 79, '       {{distri.phone}}');

  // PRODUCT LIST
  doc.autoTable({
    head: [ ['Product Code', 'Description', 'Serial No', 'Price', 'Qty', 'Total Price'] ],
    body: [
      {% for prod in product_list %}
      {% if prod.distributor == distri %}
      ['{{prod.productCode}}', '{{prod.description}}', '{{prod.serialNo}}', 'P ' + formatter.format('{{prod.totalWithTaxPerUnit}}'), '{{prod.qty}}', 'P ' + formatter.format('{{prod.totalWithTax}}')],
      {% endif %}
      {% endfor %}
      [{ content: 'Grand Total:', colSpan: 5}, {content:'P ' + formatter.format('{{estimate.overallWithTax}}'), style:{fontStyle:'bold'}}],
    ],
    startY: 85,
    theme: 'grid',
    // showHead: 'firstPage',
    columnStyles: {
      0: { minCellWidth: 20, halign: 'center' },
      1: { minCellWidth: 35, halign: 'center' },
      2: { minCellWidth: 20, halign: 'center' },
      3: { minCellWidth: 15, halign: 'center' },
      4: { CellWidth: 10, halign: 'center' },
      5: { halign: 'center' },
    },
    headStyles: { halign: 'center'},
  });

  let productY = doc.lastAutoTable.finalY;
  let numOfPayment = {{estimate.modeOfPayment}} + 1;
  let paymentheight = numOfPayment * 7.584;
  let heightLeft = productY + paymentheight + 10;
  console.log("Product Y: " + productY);
  console.log("Payment Height: " + paymentheight);
  console.log("Height Left: " + heightLeft);
  console.log("++++++++");


  if(heightLeft > 265){
    doc.addPage();
    doc.autoTable({
      head: [ ['NOTES'] ],
      body: [ ['{{estimate.poNotes | linebreaksbr  }}'.replace(regex, "\n")] ],
      headStyles: { fillColor: 'white', textColor:'black'},
      tableWidth: 110,
      pageBreak: 'avoid',
      theme: 'plain',
      tableLineWidth: 0.5,
    });
  }
  else{
    doc.autoTable({
      head: [ ['NOTES'] ],
      body: [ ['{{estimate.poNotes | linebreaksbr  }}'.replace(regex, "\n")] ],
      headStyles: { fillColor: 'white', textColor:'black'},
      startY: productY + 10,
      tableWidth: 110,
      pageBreak: 'avoid',
      theme: 'plain',
      tableLineWidth: 0.5,
    });
  }
  // NOTES SECTION
  let notesY = doc.lastAutoTable.finalY;

  if(notesY < productY){
    modeY = 14;
  }
  else{
    modeY = productY + 10;
  }

  //MODE OF PAYMENT SECTION
  doc.autoTable({
    head: [
      ['   ', 'Amount', 'Due']
    ],
    body: [
      {% with ''|center:estimate.modeOfPayment as range %}
      {% for _ in range %}
           ['','',''],
      {% endfor %}
      {% endwith %}
    ],
    headStyles: { halign: 'center', fillColor: 'gray' },
    startY: modeY,
    tableWidth: 100,
    theme: 'grid',
    margin: { left: 132 },
    pageBreak: 'auto',
    columnStyles: {
      0: {cellWidth: 20},
      1: {cellWidth: 25},
      2: {cellWidth: 25},
    },
  });

  let paymentY = doc.lastAutoTable.finalY;

  if (paymentY > notesY) {
    finalY = paymentY;
  } else if (paymentY == notesY) {
    finalY = paymentY;
  } else {
    finalY = notesY;
  }

  var pageCount = doc.internal.getNumberOfPages();
  console.log("=========================");
  console.log("Final Y: " + finalY);
  console.log("Page Count: " + pageCount);


  // REGARDS section
  if (finalY <= 196 && finalY >= 29 && pageCount == 1) {
    // Bottom First Page
    doc.text(15, 202, "Regards,");
    doc.setFontType("bold");
    doc.text(15, 216, "{{estimate.created_by.first_name}} {{estimate.created_by.last_name}} ");
    doc.setFontType("normal");
    doc.text(15, 223, "{{estimate.created_by.position}} ");
    doc.text(15, 230, "Avantgarde Technologies");
    doc.text(15, 237, "{{estimate.created_by.contact_number}} ");
    doc.text(15, 244, "{{estimate.created_by.email}} ");
    doc.text(110, 216, "Conform:");
    doc.text(110, 227, "______________________________________");
    doc.text(110, 234, "              Customer Authorized Signatory");

  } else if (finalY > 197 && finalY < 265) {
    // Top Last Page
    doc.addPage();
    doc.text(15, 20, "Regards,");
    doc.setFontType("bold");
    doc.text(15, 34, "{{estimate.created_by.first_name}} {{estimate.created_by.last_name}} ");
    doc.setFontType("normal");
    doc.text(15, 41, "{{estimate.created_by.position}} ");
    doc.text(15, 48, "Avantgarde Technologies");
    doc.text(15, 55, "{{estimate.created_by.contact_number}} ");
    doc.text(15, 62, "{{estimate.created_by.email}} ");

    doc.text(110, 34, "Conform:");
    doc.text(110, 45, "______________________________________");
    doc.text(110, 52, "              Customer Authorized Signatory");
  } else if (finalY <= 196 && finalY >= 29 && pageCount > 1) {
    // Bottom Last Page
    doc.text(15, 202, "Regards,");
    doc.setFontType("bold");
    doc.text(15, 216, "{{estimate.created_by.first_name}} {{estimate.created_by.last_name}} ");
    doc.setFontType("normal");
    doc.text(15, 223, "{{estimate.created_by.position}} ");
    doc.text(15, 230, "Avantgarde Technologies");
    doc.text(15, 237, "{{estimate.created_by.contact_number}} ");
    doc.text(15, 244, "{{estimate.created_by.email}} ");
    doc.text(110, 216, "Conform:");
    doc.text(110, 227, "______________________________________");
    doc.text(110, 234, "              Customer Authorized Signatory");
  }


  pageHeight = doc.internal.pageSize.height;
  var pageCounts = doc.internal.getNumberOfPages();

  for (i = 1; i <= pageCounts; i++) {
    doc.setFontSize(10);
    doc.setPage(i);
    doc.text(198, 272, i + "/" + pageCounts);
    doc.text(15, 272, "Address: Unit I Lennox Commercial Center Barrio Tagapo Santa Rosa City Laguna, 4026");
  }

  doc.output('dataurlnewwindow');
  {% endfor %}
}
$("#generatePDF2").on("click", genPDF3);
