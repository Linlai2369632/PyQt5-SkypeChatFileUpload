#ifndef SKYPEUPLOADER_H
#define SKYPEUPLOADER_H

#include <QWidget>

namespace Ui {
class skypeUploader;
}

class skypeUploader : public QWidget
{
    Q_OBJECT

public:
    explicit skypeUploader(QWidget *parent = nullptr);
    ~skypeUploader();

private:
    Ui::skypeUploader *ui;
};

#endif // SKYPEUPLOADER_H
