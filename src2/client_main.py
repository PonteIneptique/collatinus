import os
#include <QCoreApplication>
#include <iostream>
#include <QtWidgets>
#include <QtNetwork>

class QTcpSocket

def main(argc, argv):
    QCoreApplication a(argc, argv)
    QString req = ""
    if argc > 1:
        i = 1
        while i < argc:
            QString suite(argv[i])
            req += " " + suite
            i += 1
    else: req = "-?" # pour afficher l'aide.

    QTcpSocket * tcpSocket = new QTcpSocket()
    tcpSocket.os.abort()
    tcpSocket.connectToHost(QHostAddress::LocalHost, 5555)
    QByteArray ba = req.toUtf8()
    tcpSocket.os.write(ba)
    tcpSocket.waitForBytesWritten()
    tcpSocket.waitForReadyRead()
    ba = tcpSocket.readAll()
    tcpSocket.disconnectFromHost()
    tcpSocket.os.close()
    QString rep(ba)
    std::cout << rep.toStdString()

    a.quit()

