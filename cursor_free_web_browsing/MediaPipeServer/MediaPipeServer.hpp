#pragma once

class echo_handler : public server::handler {
    void on_message(connection_ptr con, std::string msg) {
        con->write(msg);
    }
};