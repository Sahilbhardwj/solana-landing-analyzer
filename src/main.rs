use solana_client::rpc_client::RpcClient;
use solana_sdk::{
    compute_budget::ComputeBudgetInstruction,
    signature::{read_keypair_file, Signer},
    system_instruction,
    transaction::Transaction,
};

use std::{
    thread::sleep,
    time::{Duration, Instant},
};

use serde::Serialize;
use csv;

#[derive(Serialize)]
struct TxResult {
    tx_id: u32,
    fee: u64,
    latency_ms: f64,
    estimated_slot_delay: f64,
    rpc_slot_lag: u64,
}

fn main() {

    let mut writer = csv::Writer::from_path("latency_results.csv")
        .expect("failed to create csv");

    let rpc_url = "https://api.devnet.solana.com";
    let client = RpcClient::new(rpc_url.to_string());

    let keypair = read_keypair_file("/home/sahil/.config/solana/id.json")
        .expect("Failed to read keypair");

    let priority_fees = vec![0, 500, 1000, 3000, 10000];

    println!("Starting landing + latency analysis\n");

    for fee in priority_fees {

        println!("\nTesting priority fee: {}\n", fee);

        for i in 0..20 {

            let submission_slot = client.get_slot().unwrap();

            let blockhash = client.get_latest_blockhash().unwrap();

            let transfer_ix = system_instruction::transfer(
                &keypair.pubkey(),
                &keypair.pubkey(),
                1,
            );

            let fee_ix =
                ComputeBudgetInstruction::set_compute_unit_price(fee);

            let tx = Transaction::new_signed_with_payer(
                &[fee_ix, transfer_ix],
                Some(&keypair.pubkey()),
                &[&keypair],
                blockhash,
            );

            let start = Instant::now();

            let sig = match client.send_transaction(&tx) {
                Ok(sig) => sig,
                Err(e) => {
                    println!("Failed to send transaction: {:?}", e);
                    continue;
                }
            };

            println!("TX {} sent | {}", i, sig);

            loop {

                let statuses = client.get_signature_statuses(&[sig]).unwrap();

                if let Some(status) = &statuses.value[0] {

                    let landing_slot = status.slot;

                    let rpc_slot_lag = landing_slot - submission_slot;

                    let latency = start.elapsed();

                    let latency_ms = latency.as_millis() as f64;

                    let estimated_slot_delay = latency_ms / 400.0;

                    writer.serialize(TxResult {
                        tx_id: i,
                        fee,
                        latency_ms,
                        estimated_slot_delay,
                        rpc_slot_lag,
                    }).unwrap();

                    println!(
                        "TX {} | fee {} | latency {:?} | estimated_slot_delay {:.2} | rpc lag {}",
                        i,
                        fee,
                        latency,
                        estimated_slot_delay,
                        rpc_slot_lag
                    );

                    break;
                }

                sleep(Duration::from_millis(200));
            }

            sleep(Duration::from_millis(500));
        }
    }

    writer.flush().unwrap();

    println!("\nAnalysis complete.");
}