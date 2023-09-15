#include "skypeuploader.h"
#include "ui_skypeuploader.h"

skypeUploader::skypeUploader(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::skypeUploader)
{
    ui->setupUi(this);
}

skypeUploader::~skypeUploader()
{
    delete ui;
}
